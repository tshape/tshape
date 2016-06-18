from django.contrib.auth.models import User
from django.db import models

from skills.models import Skill
from skillsets.models import Skillset
from tshape.models import BaseModel


class Profile(BaseModel):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    title = models.CharField(max_length=280)
    description = models.TextField()
    years_experience = models.IntegerField(default=0)
    skills = models.ManyToManyField(Skill)
    skillsets = models.ManyToManyField(Skillset)

    def __str__(self):
        return self.user.email

    class Meta:
        db_table = "profiles"
