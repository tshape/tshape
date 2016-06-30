from django.forms import ModelForm

from skillsets.models import Skillset


class SkillsetForm(ModelForm):

    class Meta:
        model = Skillset
        fields = '__all__'
