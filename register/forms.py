from django import forms
from registration.forms import RegistrationForm
from register.models import UserModel
from django_countries.widgets import CountrySelectWidget


class RegisterForm(RegistrationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'first_name', 'last_name', 'country']
        widgets = {
            'username': forms.Textarea(attrs={'rows': 1, 'style': 'resize:none;'}),
            'country': CountrySelectWidget()

        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
