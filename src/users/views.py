from django.contrib.auth import (
    authenticate, get_backends, login, logout, update_session_auth_hash
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic import (
    CreateView, DetailView, FormView, RedirectView, UpdateView
)
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from tshape.utils import MultiSerializerViewSetMixin, LoggedInMixin
from users.forms import (
    UserCreateForm, UserForm, UserChangePasswordForm
)
from users.models import User
from users.serializers import UserSerializer, UserUpdateSerializer


class UserViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):

    """A simple ViewSet for viewing and editing users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_action_classes = {
        'update': UserUpdateSerializer,
        'partial_update': UserUpdateSerializer,
        'destroy': UserUpdateSerializer
    }
    permission_classes = [IsAdminUser]


class LoginView(FormView):

    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            logout(request)
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user.is_active:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url(user))
        return render(self.request, self.template_name, {'form': form})

    def get_success_url(self, user, *args, **kwargs):
        return reverse_lazy('users:detail', kwargs={'username': user.username})


class LogoutView(RedirectView):

    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(self.success_url)


class SignupView(CreateView):

    form_class = UserCreateForm
    template_name = 'users/signup.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        get_backends()
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url(user))

    def get_success_url(self, user, *args, **kwargs):
        return reverse_lazy('users:detail', kwargs={'username': user.username})


class UserUpdateView(LoggedInMixin, UpdateView):

    form_class = UserForm
    template_name = 'users/edit.html'

    def get_object(self, *args, **kwargs):
        username = self.kwargs.get('username')
        if (not self.request.user.is_authenticated() or
                self.request.user.username != username):
            raise PermissionDenied
        return get_object_or_404(User, username=username)

    def form_valid(self, form, *args, **kwargs):
        form.save()
        return super(UserUpdateView, self).form_valid(form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


# only allow account owner to see email address
class UserDetailView(DetailView):

    template_name = 'users/detail.html'

    def get_object(self, *args, **kwargs):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        if (not self.request.user.is_authenticated() or
                self.request.user.username != context['user']['username']):
            context['permissions'] = True
        return context


class UserPasswordViews:

    @login_required()
    def change_password(request, *args, **kwargs):
        if request.method == 'POST':
            form = UserChangePasswordForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect(reverse('users:detail', kwargs={
                    'username': request.user.username}))
        else:
            form = UserChangePasswordForm(user=request.user)
        context = {
            'form': form,
        }
        return TemplateResponse(
            request, 'passwords/change_password.html', context)

    def reset_password(request):
        template = 'passwords/reset_password_form.html'
        email_template = 'passwords/reset_password_email.html'
        subject_template = 'passwords/reset_password_subject.txt'
        redirect = reverse('passwords:reset_password_done')
        return password_reset(request,
                              is_admin_site=False,
                              template_name=template,
                              email_template_name=email_template,
                              subject_template_name=subject_template,
                              post_reset_redirect=redirect,
                              from_email='admin@tshape.io',
                              current_app='TShape')

    def reset_password_done(request):
        return render(request, 'passwords/reset_password_done.html')

    def reset_confirm(request, username=None, token=None):
        template = 'passwords/reset_password_confirm.html'
        redirect = reverse('passwords:reset_confirm_done')
        return password_reset_confirm(request,
                                      template_name=template,
                                      username=username,
                                      token=token,
                                      post_reset_redirect=redirect)

    def reset_confirm_done(request):
        return render(request, 'passwords/reset_password_complete.html')
