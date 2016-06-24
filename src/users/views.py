from django.contrib.auth import get_backends, login, logout
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic import CreateView, FormView, RedirectView

from .forms import UserLoginForm, UserCreateForm


class LoginView(FormView):

    form_class = UserLoginForm
    success_url = reverse_lazy('profiles:index')
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            logout(request)
        return super(LoginView, self).get(request, args, kwargs)

    def form_valid(self, form):
        user = form.cleaned_data['user']
        if user.is_active:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)
        else:
            # form = UserLoginForm(self.request.POST)
            return render_to_response(self.template_name, {'form': form})

    def form_invalid(self, form):
        return render_to_response(self.template_name, {'form': form})


class LogoutView(RedirectView):

    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class SignupView(CreateView):

    form_class = UserCreateForm
    success_url = reverse_lazy('index')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return super(SignupView, self).form_valid(form)
