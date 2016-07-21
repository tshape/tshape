from django.contrib.auth import authenticate, get_backends, login, logout
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, FormView, RedirectView
from rest_framework import viewsets

from tshape.utils import MultiSerializerViewSetMixin
from users.forms import UserLoginForm, UserCreateForm
from users.models import User
from users.serializers import UserSerializer, UserUpdateSerializer


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
            return HttpResponseRedirect(self.get_success_url(user))
        else:
            # different action needed here for inactive users
            return render(self.request, self.template_name, {'form': form})

    def get_success_url(self, user, *args, **kwargs):
        return reverse_lazy('profiles:detail', kwargs={'profile_id': user.id})


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
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        get_backends()
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url(user))

    def get_success_url(self, user, *args, **kwargs):
        return reverse_lazy('profiles:detail', kwargs={'profile_id': user.id})


class UserViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_action_classes = {
        'update': UserUpdateSerializer,
        'partial_update': UserUpdateSerializer,
        'destroy': UserUpdateSerializer
    }
