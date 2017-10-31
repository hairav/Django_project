from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUp(UserCreationForm):
    first_name=forms.CharField(max_length=30,required=False,help_text='Optional')
    last_name=forms.CharField(max_length=30,required=False,help_text='Optional')
    email=forms.EmailField(max_length=254,help_text='')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password1','password2')


class LogIn(forms.Form):
   Username=forms.CharField()
   Password=forms.CharField(widget=forms.PasswordInput())
class reviewing(forms.Form):
    review=forms.CharField(max_length=500,widget=forms.Textarea())

class search (forms.Form):
    Search = forms.CharField(max_length=50)