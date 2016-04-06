from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class PasswordResetAuth(models.Model):
    choose_me = models.BooleanField(default=True)
    email = models.EmailField(max_length=75)
    token = models.CharField(max_length=11)

