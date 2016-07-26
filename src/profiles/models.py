from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from skills.models import Skill
from skillsets.models import Skillset
from tshape.models import BaseModel


class Profile(BaseModel):

    class Meta:
        db_table = 'profiles'
        ordering = ('last_name',)
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True,
                                verbose_name=_('user'),
                                on_delete=models.CASCADE)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=50)
    title = models.CharField(_('title'), max_length=280, blank=True)
    description = models.TextField(_('description'), blank=True)
    years_experience = models.IntegerField(
        _('years of experience'), null=True, blank=True)
    skills = models.ManyToManyField(Skill, verbose_name=_('skills'))
    skillsets = models.ManyToManyField(Skillset, verbose_name=_('skillsets'))

    def clean(self):
        if skills:
            orphaned_skills = any(skill.skillset_id not in self.skillset_ids
                                  for skill in self.skills)
            if orphaned_skills:
                raise ValidationError(
                    {'skills': _('Corresponding skillset must be attached to profile before skill.')})
            # raise ValidationError({'skills': _('User cannot have more than 10 skills for a one skillset')}) if any([skill.skillset_id not in self.skillset_ids for skill in self.skills])

    @property
    def skillset_ids(self):
        return [skillset.id for skillset in self.skillsets.all()]

    @property
    def skill_ids(self):
        return [skill.id for skill in self.skills.all()]

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
