from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

class UserCreationForm(forms.ModelForm):

    username = forms.CharField(disabled=True)
    email = forms.EmailField(disabled=True)
    first_name = forms.CharField(disabled=True)
    last_name = forms.CharField(disabled=True)
    isStudent = forms.BooleanField(widget = forms.HiddenInput())
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    token = forms.CharField(widget = forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
