from django import forms
from member.models import User

class PermissionForm(forms.ModelForm):
    class Meta:
        model =User
        fields=('username','is_member')