from typing import Any
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm

from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput

from django_recaptcha.fields import ReCaptchaField


#registration form

class CreateUserForm(UserCreationForm):

    class Meta:

        model = User

        fields = ['username', 'email', 'password1', 'password2']

    captcha = ReCaptchaField()


    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        #making email required

        self.fields['email'].required = True


#email validaiton

    def clean_email(self):

        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():

            raise forms.ValidationError('This email is invalid')
        
        if len(email) >= 350:

            raise forms.ValidationError('your email is too long') 
        
        return email





#login form
    

class LoginForm(AuthenticationForm):


    username = forms.CharField(widget=TextInput())

    password = forms.CharField(widget=PasswordInput())



#update form
    
class UpdateUserForm(forms.ModelForm):

    password = None

    def __init__(self, *args, **kwargs):
        
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        #making email required

        self.fields['email'].required = True


    class Meta:

        model = User

        fields = ['username', 'email']

        exclude = ['password1', 'password2']


    #email validaiton

    def clean_email(self):
        
        email = self.cleaned_data.get('email')
        instance = getattr(self, 'instance', None)

        if instance and User.objects.filter(email=email).exclude(pk=instance.pk).exists():
            raise forms.ValidationError('This email is invalid')
            
        if len(email) >= 350:
            raise forms.ValidationError('Your email is too long') 
            
        return email