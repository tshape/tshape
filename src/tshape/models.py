from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):

    class Meta:
        abstract = True

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
