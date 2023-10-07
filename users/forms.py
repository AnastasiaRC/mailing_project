from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from mailing.forms import StyleFormMixin
from users.models import User
from django import forms


class UserForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Регистрация пользователя"""
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(StyleFormMixin, UserForm, UserChangeForm):
    """Редактирование профиля пользователя"""
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'іmage', 'phone')


class UserStatusForm(StyleFormMixin, UserForm, UserChangeForm):
    """Управление статусом пользователя"""
    class Meta:
        model = User
        fields = ('is_active',)