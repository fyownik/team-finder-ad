from urllib.parse import urlparse

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from .constants import GITHUB_HOST, GITHUB_URL_ERROR


User = get_user_model()


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Пароль'
    )

    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        required=False,
        widget=forms.HiddenInput
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput
    )
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=email,
                password=password,
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'name',
            'surname',
            'avatar',
            'about',
            'phone',
            'github_url',
        )

    def clean_github_url(self):
        github_url = self.cleaned_data.get('github_url')
        if github_url:
            netloc = urlparse(github_url).netloc.lower()
            valid_hosts = {GITHUB_HOST, f'www.{GITHUB_HOST}'}
            if netloc not in valid_hosts:
                raise forms.ValidationError(GITHUB_URL_ERROR)
        return github_url
