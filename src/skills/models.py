from django.db import models

from skillsets.models import Skillset
from tshape.models import BaseModel


class Skill(BaseModel):

    name = models.CharField(max_length=280)
    description = models.TextField()
    verified = models.BooleanField(null=False, default=False)
    skillset_id = models.ForeignKey(
        Skillset, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "skills"
