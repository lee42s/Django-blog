from django import forms
from .models import Post,Notice_category
from ckeditor.widgets import CKEditorWidget

from ckeditor.fields import RichTextField
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title','content','category']
        widgets = {
            'title':forms.TextInput(attrs={'class':'title','placeholder': '제목'}),
            'content':forms.CharField(widget=CKEditorWidget()),
        }
        labels = {
            'title': '제목',
            'content': '내용',
            'category':'게시판 이름'
        }

class Notice_categoryForm(forms.ModelForm):
    class Meta:
        model = Notice_category
        fields = ('title','list_auth','detail_auth','writer_auth')