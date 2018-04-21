from django.contrib import admin
from notice.models import Post,Notice_category,Word_filtering
from django import forms
from ckeditor.widgets import CKEditorWidget
# Register your models here.
admin.site.register(Post)
admin.site.register(Notice_category)
admin.site.register(Word_filtering)