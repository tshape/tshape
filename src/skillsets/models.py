from django.db import models


class Skillset(models.Model):

    name = models.CharField(max_length=280)
    description = models.TextField()
    verified = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.name
