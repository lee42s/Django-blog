from django.db import models
from member.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils import timezone
import os
# Create your models here.

class Notice_category(models.Model):
    title=models.CharField(verbose_name='제목',max_length=100)
    level1 = 1
    level2 = 2
    level3 = 3
    LEVEL_TYPE_CHOICES = (
        (level1, '최고 권한'),
        (level2, '일반 권한'),
        (level3, '최하위 권한'),
    )
    list_auth = models.IntegerField('목록보기', choices=LEVEL_TYPE_CHOICES, null=True, blank=True)
    detail_auth = models.IntegerField('상세보기', choices=LEVEL_TYPE_CHOICES, null=True, blank=True)
    writer_auth = models.IntegerField('글쓰기', choices=LEVEL_TYPE_CHOICES, null=True, blank=True)
    created_date = models.DateTimeField(verbose_name='만든날짜',auto_now_add=True,)  # auto_now_add=True생정날짜,auto_now=True수정날짜
    modified_date = models.DateTimeField(verbose_name='수정날짜', auto_now=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    category = models.ForeignKey(Notice_category,verbose_name='카테고리',default='',on_delete=models.CASCADE)
    author=models.ForeignKey(User,verbose_name='작성자',on_delete=models.CASCADE)
    title = models.CharField(verbose_name='제목',max_length=200,default="")
    content = models.TextField(verbose_name='내용',default="")
    created_date=models.DateTimeField(verbose_name='만든날짜',auto_now_add=True)#auto_now_add=True생정날짜,auto_now=True수정날짜
    modified_date = models.DateTimeField(verbose_name='수정날짜',auto_now=True)

    def __str__(self):
        return self.title

class File(models.Model):
    file =models.FileField(upload_to='files/%Y/%m/%d/',null=True)
    created_date =models.DateTimeField(auto_now_add=True)
    post =models.ForeignKey(Post, null=True, on_delete=models.CASCADE)

    def filename(self):
        return os.path.basename(self.file.name)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super(File,self).delete(*args, **kwargs)

    def __str__(self):
        return  self.file.name

class Imges(models.Model):
    imges =models.ImageField(upload_to='imges/%Y/%m/%d/',height_field=None, width_field=None,null=True)
    created_date =models.DateTimeField(auto_now_add=True)
    post =models.ForeignKey(Post, null=True, on_delete=models.CASCADE)

    def imgename(self):
        return os.path.basename(self.imges.name)

    def delete(self, *args, **kwargs):
        self.imges.delete()
        super(Imges,self).delete(*args, **kwargs)

    def __str__(self):
        return  self.imges.name


class Comment(models.Model):
    author = models.ForeignKey(User, verbose_name='작성자', on_delete=models.CASCADE,default='')
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    text=models.TextField()
    created_date = models.DateTimeField(verbose_name='만든날짜', auto_now_add=True)

    def __str__(self):
        return self.text


class Word_filtering(models.Model):
    text = models.TextField(verbose_name='내용')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
