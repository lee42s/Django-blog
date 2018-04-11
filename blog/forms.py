from member.models import User
from django.contrib.auth.forms import UserCreationForm,UsernameField,UserChangeForm,ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django import forms
class CreateUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email','first_name','last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'username', 'placeholder': '15자 이내로 입력 가능합니다.'}),
            'email': forms.EmailInput(attrs={'class': 'email','placeholder': 'aaa@aaa.aaa'}),
            'first_name':forms.TextInput(attrs={'class': 'first_name', 'placeholder': '2자 이내로 입력 가능합니다.'}),
            'last_name': forms.TextInput(attrs={'class': 'last_name', 'placeholder': '2자 이내로 입력 가능합니다.'}),
        }
        labels = {
            'username': '아이디',
            'first_name':'성',
            'last_name':'이름',
            'email': '이메일',
        }
    # 글자수 제한
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__( *args, **kwargs)
        self.fields['username'].widget.attrs['maxlength'] = 8
        self.fields['first_name'].widget.attrs['maxlength'] = 2
        self.fields['last_name'].widget.attrs['maxlength'] = 2


