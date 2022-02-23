from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    email = models.EmailField(
        _('Email addres'), unique=True
    )
    first_name = models.CharField(_('first name'), max_length=150, null=False, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, null=True, blank=True)
    phone_number = PhoneNumberField(verbose_name='Номер телефона', unique=True, null=False, blank=False)

    email_verify = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name_plural = 'Пользователи'


class EmailsForMessages(models.Model):
    email = models.EmailField(
        verbose_name='Email', help_text='Email пользователя, которому нужно отправлять сообщения о заказах',
        null=False, blank=False
    )

    class Meta:
        verbose_name_plural = ' Почта для уведомлений'

    def __str__(self):
        return self.email
