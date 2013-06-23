from django.db import models
from django.contrib.auth.models import User

class Credential(models.Model):
    user = models.ForeignKey(User, related_name='webapi_credential')
    credential=models.CharField(max_length=256)

