from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from .models import User


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'title',
                  'email', 'password1', 'password2')

    title = forms.CharField(label=_('Job Title'), required=False)
    email = forms.EmailField(label=_('E-mail'), max_length=75, required=True)

    def save(self, commit=True):
        data = dict(self.cleaned_data)
        data['password'] = data.pop('password1')
        password2 = data.pop('password2')
        if password2 != data['password']:
            raise forms.ValidationError(
                _('Password fields do not match.'),
                code='invalid')
        return User.objects.create(**data)


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'title', 'email')

    username = forms.CharField(label=_('Username'), required=True)
    title = forms.CharField(label=_('Job Title'), required=False)
    email = forms.EmailField(label=_('E-mail'), max_length=75, required=True)


class UserLimitedForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'title')

    username = forms.CharField(label=_('Username'), required=True)
    title = forms.CharField(label=_('Job Title'), required=False)


class UserChangePasswordForm(forms.Form):

    password1 = forms.CharField(
        widget=forms.PasswordInput, label=_('New Password'), required=True)
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label=_('Confirm New Password'), required=True)

    def __init__(self, user, *args, **kwargs):
        self.user = User.objects.get(username=user.username)
        super(UserChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    _('Password fields must match.'),
                    code='password_mismatch',
                )
        return self.cleaned_data

    def save(self):
        self.user.set_password(self.cleaned_data['password1'])
        self.user.save()
