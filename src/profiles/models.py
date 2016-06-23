from django.db import models
from django.utils.translation import ugettext_lazy as _

from skills.models import Skill
from skillsets.models import Skillset
from tshape.models import BaseModel
from users.models import User


class Profile(BaseModel):

    class Meta:
        db_table = 'profiles'
        ordering = ('last_name',)
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    user = models.OneToOneField(User, verbose_name=_('user'),
                                on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=50)
    title = models.CharField(_('title'), max_length=280)
    description = models.TextField(_('description'))
    years_experience = models.IntegerField(_('years of experience'), null=True)
    skills = models.ManyToManyField(Skill, verbose_name=_('skills'))
    skillsets = models.ManyToManyField(Skillset, verbose_name=_('skillsets'))

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
