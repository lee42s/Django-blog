from django import forms
from .models import Post
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

