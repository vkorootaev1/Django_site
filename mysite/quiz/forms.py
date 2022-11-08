from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):

    def clean(self):
        current_flat = self.cleaned_data.get('flat')
        max_flat = self.cleaned_data.get('house').max_flat
        if current_flat > max_flat:
            raise forms.ValidationError("Недопустимый номер квартиры")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "password1", "password2", "house", "flat")
        help_texts = {
            'username': None,
            'password2': 'None',
            'password1': None
        }


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email", "username", "password", "house", "flat")


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль')
