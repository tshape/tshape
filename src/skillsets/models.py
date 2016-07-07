from django.db import models
from django.utils.translation import ugettext_lazy as _

from tshape.models import BaseModel


class Skillset(BaseModel):

    class Meta:
        db_table = 'skillsets'
        ordering = ('name',)
        verbose_name = _('skillset')
        verbose_name_plural = _('skillsets')

    name = models.CharField(
        _('name'), null=False, unique=True, max_length=280,
        error_messages={
            'unique': _("A user with that email already exists."),
        })
    description = models.TextField(_('description'))
    verified = models.BooleanField(_('verified'), null=False, default=False)
    weight = models.IntegerField(_('weight'), null=False, default=0)

    def __str__(self):
        return self.name
