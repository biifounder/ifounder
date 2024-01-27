from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, DateInput, TimeInput
from.models import *
from .models import  User


class ProjectForm(forms.ModelForm):
    name =  forms.CharField(label="Name",required=True)
    description = forms.CharField(label="Description", required=False,help_text="", widget=forms.Textarea(attrs={'rows': 10, 'cols': 85}))
    class Meta: 
        model = Project
        fields = ['name', 'description']  

class MyUserCreationForm(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'id':'password1', 'placeholder': 'كلمة المرور'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'id':'password2','placeholder': 'تأكيد كلمة المرور'}))

    class Meta:
        model = User
        fields = ['password1', 'password2']
        widgets = {
            'password1': forms.TextInput(attrs={'placeholder': 'كلمة المرور'}), 
            'password2': forms.TextInput(attrs={'placeholder': 'تأكيد كلمة المرور'}), 
        }

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
        }
