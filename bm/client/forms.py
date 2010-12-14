from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from bm.client.RPCQuerySet import RPCQuerySet

class MessageForm(forms.Form):
    user_to = forms.ModelChoiceField(RPCQuerySet("Player"))
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget = forms.Textarea())
    
class UserForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    
class RegistrationForm(UserCreationForm):
    email = fields.EmailField()