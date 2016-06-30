from django.forms import ModelForm

from skills.models import Skill


class SkillForm(ModelForm):

    class Meta:
        model = Skill
        fields = '__all__'
