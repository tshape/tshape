from django.db import models
from django.utils.translation import ugettext_lazy as _

from skillsets.models import Skillset
from tshape.models import BaseModel


class Skill(BaseModel):

    class Meta:
        db_table = 'skills'
        ordering = ('name',)
        verbose_name = _('skill')
        verbose_name_plural = _('skills')

    name = models.CharField(
        _('name'), null=False, unique=True, max_length=280,
        error_messages={
            'unique': _('A skill with that name already exists.'),
        })
    description = models.TextField(_('description'))
    verified = models.BooleanField(_('verified'), null=False, default=False)
    skillset = models.ForeignKey(
        Skillset, verbose_name=_('skillset'),
        related_name='skills', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name
