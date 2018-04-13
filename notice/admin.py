from django.contrib import admin
from notice.models import Post
from django import forms
from ckeditor.widgets import CKEditorWidget
# Register your models here.
admin.site.register(Post)