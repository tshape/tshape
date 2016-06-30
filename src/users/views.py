from django.contrib.auth import authenticate, get_backends, login, logout
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, FormView, RedirectView
from rest_framework import viewsets

from users.forms import UserLoginForm, UserCreateForm
from users.models import User
from users.serializers import UserSerializer


class LoginView(FormView):

    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            logout(request)
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.cleaned_data['user']
        if user.is_active:
            login(self.request, user)
            context = {'profile_id': user.id}
            return HttpResponseRedirect(
                reverse(self.get_success_method(user), kwargs=context))
        else:
            # different action needed here for inactive users
            return render(self.request, self.template_name, {'form': form})

    def get_success_method(self, user, *args, **kwargs):
        if hasattr(user, 'profile'):
            return 'profiles:detail'
        else:
            return 'profiles:new'


class LogoutView(RedirectView):

    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class SignupView(CreateView):

    form_class = UserCreateForm
    success_url = reverse_lazy('profiles:new')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        get_backends()
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return super(SignupView, self).form_valid(form)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
