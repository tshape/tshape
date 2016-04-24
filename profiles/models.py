from django.db import models

# Create your models here.
class Profile(models.Model):
    profile_text = models.CharField(max_length=200)
    profile_body = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('date published')