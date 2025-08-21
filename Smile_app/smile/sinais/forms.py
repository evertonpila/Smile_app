from django import forms
from django.contrib.auth.models import User
from .models import CredenciaisAPI

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class CredenciaisForm(forms.ModelForm):
    class Meta:
        model = CredenciaisAPI
        fields = ['chave_api', 'chave_secreta']
        widgets = {
            'chave_api': forms.TextInput(attrs={'class': 'form-control'}),
            'chave_secreta': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
