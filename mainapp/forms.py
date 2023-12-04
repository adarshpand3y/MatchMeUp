from django import forms 
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
  
# creating a form 

class DetailsForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        # fields = ['gender', 'bio', 'pic1', 'pic2', 'pic3']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # Set the 'required' attribute to True for the ImageField
            self.fields['pic1'].widget.attrs['required'] = True
            self.fields['pic2'].widget.attrs['required'] = True
            self.fields['pic3'].widget.attrs['required'] = True

class CreateUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)