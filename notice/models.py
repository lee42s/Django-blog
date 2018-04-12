from django.db import models
from member.models import User
from djrichtextfield.models import RichTextField
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    author=models.ForeignKey(User,verbose_name='작성자')
    title = models.CharField(verbose_name='제목',max_length=200,default="")
    text= RichTextField(verbose_name='내용',default='')
    created_date=models.DateTimeField(verbose_name='만든날짜',auto_now_add=True)#auto_now_add=True생정날짜,auto_now=True수정날짜
    modified_date = models.DateTimeField(verbose_name='수정날짜',auto_now=True)
    post_is_manager=models.BooleanField(verbose_name='관리자',default=False)
    post_is_member = models.BooleanField(verbose_name='회원', default=False)


    def __str__(self):
        return self.title