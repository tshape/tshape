from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, FormView, RedirectView


class LoggedInMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


@require_http_methods(["GET", "POST"])
def index(request):
    return render(request, "tshape/index.html")


class LoginView(FormView):

    form_class = AuthenticationForm
    success_url = reverse_lazy('index')
    template_name = 'tshape/login.html'

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
    template_name = 'tshape/signup.html'
