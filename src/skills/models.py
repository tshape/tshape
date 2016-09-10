from django.core.exceptions import ValidationError
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
        unique_together = ('name', 'skillset',)

    name = models.CharField(
        _('name'), null=False, max_length=280)
    description = models.TextField(_('description'), blank=True, default='')
    verified = models.BooleanField(_('verified'), null=False, default=False)
    weight = models.IntegerField(_('weight'), null=True, blank=True)
    skillset = models.ForeignKey(
        Skillset, verbose_name=_('skillset'),
        related_name='skills', on_delete=models.CASCADE, null=False)

    def clean(self):
        if self.verified and not self.weight:
            raise ValidationError(
                {'skills': _('Verified skills must have a weight.')})

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Skill, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
