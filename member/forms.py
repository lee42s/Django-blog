from django import forms
from member.models import User

class PermissionForm(forms.ModelForm):
    class Meta:
        model =User
        fields=('is_member','is_manager','is_level')
        widgets = {
            'is_member': forms.CheckboxInput(attrs={'class':'is_member'}),
            'is_manager': forms.CheckboxInput(attrs={'class': 'is_manager' }),
            'is_level':forms.Select(attrs={'class': 'is_level form-control' })
        }
        labels = {
            'is_member':'회원',
            'is_manager': '관리자',
            'is_level':'회원등급'
        }