from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Application

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username","email","password1","password2")

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ("name","email","resume")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder":"Your name"}),
            "email": forms.EmailInput(attrs={"placeholder":"you@example.com"}),
        }
    def clean_name(self):
        v = self.cleaned_data.get("name","").strip()
        if not v: raise forms.ValidationError("Name is required.")
        return v
    def clean_email(self):
        v = self.cleaned_data.get("email","").strip()
        if not v: raise forms.ValidationError("Email is required.")
        return v