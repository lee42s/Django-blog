from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_manager = models.BooleanField('관리자', default=False)
    is_member = models.BooleanField('회원', default=False)

    level1 =1
    level2 = 2
    level3 = 3
    LEVEL_TYPE_CHOICES = (
        (level1,'최고 권한'),
        (level2, '일반 권한'),
        (level3, '최하위 권한'),
    )
    is_level = models.IntegerField('권한레벨',choices=LEVEL_TYPE_CHOICES,null=True,blank=True)

