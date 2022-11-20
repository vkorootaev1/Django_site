from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm, \
    SetPasswordForm
from django.core.exceptions import ValidationError

from .models import User, House, Answer, answer_choice
from .utils import send_email_for_verify


class CustomUserCreationForm(UserCreationForm):

    # def __init__(self, *args, **kwargs):
    #     super(CustomUserCreationForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        label="Email",
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", 'placeholder': 'email'}
        ),
    )

    username = forms.CharField(
        label="Имя пользователя",
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", 'placeholder': 'Имя пользователя'}
        ),
    )

    first_name = forms.CharField(
        label="Ваше имя",
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", 'placeholder': 'Ваше имя'}
        ),
    )

    last_name = forms.CharField(
        label="Ваша фамилия",
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", 'placeholder': 'Ваша фамилия'}
        ),
    )

    password1 = forms.CharField(
        label="Придумайте пароль",
        max_length=30,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", 'placeholder': 'Пароль'}
        ),
    )

    password2 = forms.CharField(
        label="Повторите пароль",
        max_length=30,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", 'placeholder': 'Повторите пароль'}
        ),
    )

    house = forms.ModelChoiceField(
        label='Дом',
        empty_label='Выберите ваш дом',
        queryset=House.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
    )

    flat = forms.IntegerField(
        label="Номер квартиры",
        widget=forms.NumberInput(
            attrs={"class": "form-control", 'placeholder': 'Введите номер квартиры'}
        ),
    )

    def clean(self):
        print(self)
        current_flat = self.cleaned_data.get('flat')
        max_flat = self.cleaned_data.get('house').max_flat
        if current_flat > max_flat:
            msg = "Введите правильный номер квартиры"
            self.add_error('flat', msg)

        email = self.cleaned_data.get('email')
        if User.objects.get(email=email):
            msg = "Упс... Email уже зарегистрирован"
            self.add_error('email', msg)

        username = self.cleaned_data.get('username')
        if User.objects.get(username=username):
            msg = "Имя пользователя уже занято"
            self.add_error('username', msg)
        return self.cleaned_data

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "password1", "password2", "house", "flat")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "username", "password", "house", "flat")


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль')


class MyAuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if not self.user_cache.email_verify:
                send_email_for_verify(self.request, self.user_cache)
                raise ValidationError(
                    'Ваш Email не верифицирован? Пожалуйста, проверьте свою электронную почту',
                    code='invalid_login',
                )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class MyPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(MyPasswordChangeForm, self).__init__(*args, **kwargs)

    error_messages = {
        **SetPasswordForm.error_messages,
        "password_incorrect": "Ваш старый пароль некорректный, пожалуйста, попробуйте снова"
    }

    old_password = forms.CharField(
        label="Старый пароль",
        max_length=30,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", 'placeholder': 'Старый пароль'}
        ),
    )

    new_password1 = forms.CharField(
        label="Новый пароль",
        max_length=30,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", 'placeholder': 'Новый пароль'}
        ),
    )

    new_password2 = forms.CharField(
        label="Повторите новый пароль",
        max_length=30,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", 'placeholder': 'Новый пароль'}
        ),
    )

    field_order = ["old_password", "new_password1", "new_password2"]


class AnswerForm(forms.Form):
    answer = forms.ChoiceField(
        label='Ответ',
        choices=answer_choice,
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
    )

