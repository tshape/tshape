from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):

    class Meta:
        abstract = True

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    # def save(self, *args, **kwargs):
    #     if not self.created_at:
    #         self.created_at = timezone.now()
    #     self.updated_at = timezone.now()
    #     return super(BaseModel, self).save(*args, **kwargs)
