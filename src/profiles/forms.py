from django import forms

from profiles.models import Profile
from skills.models import Skill
from skillsets.models import Skillset


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ['user', 'skills', 'skillsets']

    # def __init__(self, *args, **kwargs):
    #     user_id = self.kwargs.get('user')
    #     if user_id:


class ProfileTShapeForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['skillsets', 'skills']

    skillsets = forms.ModelMultipleChoiceField(queryset=Skillset.objects.all())
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all())
