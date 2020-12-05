# from django.contrib.auth.models import User
from account.models import MyUser, Request
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    # email = forms.EmailField()
    # first_name = forms.CharField()
    # last_name = forms.CharField()

    class Meta:
        model = MyUser
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'profile_image']

class AuthorRequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ['message']