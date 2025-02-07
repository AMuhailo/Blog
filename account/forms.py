import email
from django import forms
from .models import Profile
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    password2 = forms.CharField(widget = forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password2'] != cd['password']:
            raise forms.ValidationError("Password don`t similar.Please again!")
        return cd['password']
    
    def clean_email(self):
        cd = self.cleaned_data['email']
        if User.objects.filter(email=cd).exists():
            raise forms.ValidationError('Email already in use!')
        return cd
        
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','birthday']
        widgets = {
        'image':forms.FileInput(attrs={
            'class':'form-control',
            'id':'inputGroupFile02'
            }),
        'birthday':forms.DateInput(attrs={
            'class':'form-control',
            'aria-describedby':'basic-addon1',
            'type':'date'
        })
            }
class UserDataEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email']
        widgets = {
        'first_name':forms.TextInput(attrs={
            'class':'form-control',
            'type':'text',
            'placeholder':'First name', 
            }),
        'last_name':forms.TextInput(attrs={
            'class':'form-control',
            'type':'text',
            'placeholder':'Last name', 
            }),
        'email':forms.EmailInput(attrs={
            'class':'form-control',
            'type':'email',
            'placeholder':'name@gmail.com', 
            'aria-describedby':'basic-addon4',
        })
        }
    
    def clean_email(self):
        cd = self.cleaned_data['email']
        if User.objects.exclude(id = self.instance.id).filter(email=cd).exists():
            raise forms.ValidationError("Email already in use!")
        return cd