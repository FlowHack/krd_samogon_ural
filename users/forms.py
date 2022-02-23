from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm,
    AuthenticationForm as DjangoAuthenticationForm
)
from django.contrib.auth import authenticate
from .utils import send_email_for_verify
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

User = get_user_model()


class AuthenticationForm(DjangoAuthenticationForm):
    username = forms.EmailField(
        label=_('Email address'),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                email=username,
                password=password
            )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

            if not self.user_cache.email_verify:
                send_email_for_verify(self.request, self.user_cache)
                raise ValidationError(
                    'У вас не подтверждён Email? Проверьте свою почту!',
                    code='email',
                    params={'username': self.username_field.verbose_name}
                )

        return self.cleaned_data


class UserCreationForm(DjangoUserCreationForm):
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    phone_number = PhoneNumberField(label='Номер телефона')

    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'phone_number')
