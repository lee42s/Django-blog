from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    is_manager = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
