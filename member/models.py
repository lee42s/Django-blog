from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_manager = models.BooleanField('관리자',default=False)
    is_member = models.BooleanField('회원',default=False)

