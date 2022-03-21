from django.contrib import admin
from .models import User, EmailsForMessages
from users.forms import UserCreationForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('username', 'email', 'first_name', 'phone_number', 'password1', 'password2'),
            }
        )
    )
    add_form = UserCreationForm

    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('email', 'username')
    list_filter = ('first_name',)
    empty_value_display = '-пусто-'


@admin.register(EmailsForMessages)
class EmailsForMessagesAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)
    list_filter = ('email',)
    empty_value_display = '-пусто-'
