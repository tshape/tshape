from django.forms import ModelForm

from profiles.models import Profile


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        exclude = ['user', 'skills', 'skillsets']

    # def __init__(self, *args, **kwargs):
    #     user_id = self.kwargs.get('user')
    #     if user_id:
