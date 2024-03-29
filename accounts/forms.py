from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    re_password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('re_password')
        if p1 is None or p2 is None or p1 != p2:
            raise ValidationError('Podane hasła nie są takie same.')
        if len(first_name) < 3:
            raise ValidationError('Podane imię jest za krótkie')
        if len(last_name) < 3:
            raise ValidationError('Podane nazwisko jest za krótkie')
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
