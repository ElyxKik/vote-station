from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True)
    email_confirmed = models.BooleanField(default=False)

