from django import forms
from django.contrib.auth.models import User

class UserCreationForm(forms.ModelForm):

    username = forms.CharField(disabled=True)
    email = forms.EmailField(disabled=True)
    first_name = forms.CharField(disabled=True)
    last_name = forms.CharField(disabled=True)
    password = forms.PasswordInput()
    confirm_password = forms.PasswordInput()


    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password', 'confirm_password']
