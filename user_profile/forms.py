from django import forms
from register.models import UserModel
from django_countries.widgets import CountrySelectWidget

# form for editing profile
from user_profile.models import Report


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'first_name', 'last_name', 'country', 'avatar', 'description']
        widgets = {
            'username': forms.Textarea(attrs={'rows': 1, 'style': 'resize:none;'}),
            'description': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'country': CountrySelectWidget(),

        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['message', 'image', 'type']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),

        }
