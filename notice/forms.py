from django import forms
from .models import Post,Notice_category,Word_filtering
from ckeditor.widgets import CKEditorWidget

from ckeditor.fields import RichTextField
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title','content']
        widgets = {
            'title':forms.TextInput(attrs={'class':'title','id':'title','placeholder': '제목을 입력하세요'}),
            'content':forms.Textarea(attrs={'class':'content','id':'content','placeholder': '내용을 입력하세요'}),
        }
        labels = {
            'title': '제목',
            'content': '내용',
        }

class Word_filteringForm(forms.ModelForm):
    class Meta:
        model = Word_filtering
        fields = ['text']

# class CommentForm(forms.ModelForm):
#
#     class Meta:
#         model = Comment
#         fields = ['text']
#         widgets = {
#             'text': forms.Textarea(attrs={'class': 'text', 'placeholder': '내용을 입력해주세요'}),
#         }
#         labels = {
#             'text':'내용'
#         }
#     def __init__(self, *args, **kwargs):
#         super(CommentForm, self).__init__(*args, **kwargs)
#         self.fields['text'].widget.attrs['maxlength'] = 8


class Notice_categoryForm(forms.ModelForm):
    class Meta:
        model = Notice_category
        fields = ['title','list_auth','detail_auth','writer_auth']