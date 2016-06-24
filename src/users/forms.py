from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _

from .models import User


class UserLoginForm(AuthenticationForm):

    email = forms.EmailField(label=_('E-mail'), max_length=75)
    password = forms.CharField(
        widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError(
                _('Invalid email or password. Please try again.'),
                code='invalid')
        cleaned_data['user'] = user
        return cleaned_data


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    email = forms.EmailField(required=True)
