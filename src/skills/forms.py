from django import forms

from skills.models import Skill


class SkillForm(forms.ModelForm):

    class Meta:
        model = Skill
        fields = '__all__'
