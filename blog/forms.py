from member.models import User
from django.contrib.auth.forms import UserCreationForm,UsernameField,UserChangeForm,ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model

class CreateUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email','first_name','last_name']
        field_classes = {'username': UsernameField}
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


