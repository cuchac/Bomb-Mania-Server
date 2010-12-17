from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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
    
    def __init__(self, *args, **kwargs):
        ret = super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "Fighter Name"
        self.fields["username"].help_text = ""
        self.fields["password2"].help_text = ""
        return ret
    
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        ret = super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "Fighter Name"
        self.fields["username"].help_text = ""
        return ret