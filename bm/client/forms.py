from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields

class MessageForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    
class UserForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    
class RegistrationForm(UserCreationForm):
    email = fields.EmailField()