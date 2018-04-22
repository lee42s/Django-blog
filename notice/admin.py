from django.contrib import admin
from notice.models import Post,Notice_category,Word_filtering,Comment,File,Imges
from django import forms
from ckeditor.widgets import CKEditorWidget
# Register your models here.
admin.site.register(Post)
admin.site.register(Notice_category)
admin.site.register(Word_filtering)
admin.site.register(Comment)
admin.site.register(File)
admin.site.register(Imges)