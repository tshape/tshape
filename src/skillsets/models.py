from django.db import models

from tshape.models import BaseModel


class Skillset(BaseModel):

    name = models.CharField(max_length=280)
    description = models.TextField()
    verified = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.name
