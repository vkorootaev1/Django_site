from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm, \
    SetPasswordForm, PasswordResetForm
from django.core.exceptions import ValidationError

from .models import User, House, Answer, answer_choice
from .utils import send_email_for_verify


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        current_flat = self.cleaned_data.get('flat')
        max_flat = self.cleaned_data.get('house').max_flat
        if current_flat > max_flat:
            msg = "Введите правильный номер квартиры"
            self.add_error('flat', msg)

        email = self.cleaned_data.get('email')
        print(User.objects.filter(email=email).count())
        if User.objects.filter(email=email).count():
            msg = "Упс... Email уже зарегистрирован"
            self.add_error('email', msg)

        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).count():
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


class MyAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                if not self.user_cache.email_verify:
                    send_email_for_verify(self.request, self.user_cache)
                    raise ValidationError(
                        'Ваш Email не верифицирован? Пожалуйста, проверьте свою электронную почту',
                        code='invalid_login',
                    )
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


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        label='Адрес электронной почты',
        widget= forms.EmailInput(
            attrs={'class': 'form-control'}
        ),
    )


class MySetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(MySetPasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
