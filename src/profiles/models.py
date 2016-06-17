from django.contrib.auth.models import User
from django.db import models

from tshape.models import BaseModel


class Profile(BaseModel):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=280)
    description = models.TextField()
    years_experience = models.IntegerField(default=0)

    def __str__(self):
        return self.title
