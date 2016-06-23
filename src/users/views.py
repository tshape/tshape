from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, FormView, RedirectView


class LoginView(FormView):

    form_class = AuthenticationForm
    success_url = reverse_lazy('index')
    template_name = 'users/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return self.form_invalid(form)


class LogoutView(RedirectView):

    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class SignupView(CreateView):

    form_class = UserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'users/signup.html'
