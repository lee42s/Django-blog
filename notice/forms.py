from django import forms
from .models import Post,Notice_category,Word_filtering,Comment,File,Imges
from ckeditor.widgets import CKEditorWidget

from ckeditor.fields import RichTextField
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title','content']
        widgets = {
            'title':forms.TextInput(attrs={'class':'title','id':'title','placeholder': '제목을 입력하세요'}),
            'content':forms.CharField(widget=CKEditorWidget()),
        }
        labels = {
            'title': '제목',
            'content': '내용',
        }

class FlieForm(forms.ModelForm):
    class Meta:
        model =File
        fields =['file',]

class ImgesForm(forms.ModelForm):
    class Meta:
        model =Imges
        fields =['imges',]
      
class Word_filteringForm(forms.ModelForm):
    class Meta:
        model = Word_filtering
        fields = ['text']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'comment', 'placeholder': '댓글 을 입력해주세요','row':0,'cols':100,'style':'resize:none;'}),
        }
        labels = {
            'text':'댓글'
        }
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['maxlength'] = 200


class Notice_categoryForm(forms.ModelForm):
    class Meta:
        model = Notice_category
        fields = ['title','list_auth','detail_auth','writer_auth']
