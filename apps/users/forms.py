from django import forms
from django.contrib.auth import authenticate
from .models import User


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(),
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Invalid email or password.')
        return cleaned_data


class EmailRegistrationForm(forms.Form):
    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    first_name = forms.CharField(
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        min_length=5,
        max_length=70,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password_confirmation = forms.CharField(
        min_length=5,
        max_length=70,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email already exists")
        return email

    def clean(self):
        data = super().clean()
        if data['password'] != data['password_confirmation']:
            raise forms.ValidationError("Passwords don't match")
        return data

    def save(self):
        data = self.cleaned_data
        data.pop('password_confirmation')
        return User.objects.create_user(**data)
