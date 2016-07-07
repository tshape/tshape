from django import forms

from skillsets.models import Skillset


class SkillsetForm(forms.ModelForm):

    class Meta:
        model = Skillset
        fields = '__all__'


SkillsetFormSet = forms.modelformset_factory(Skillset, form=SkillsetForm)
