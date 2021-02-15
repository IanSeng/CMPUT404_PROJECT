from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from main import models 

class UserAdmin(BaseUserAdmin):
    ordering=['id']
    list_display=["username", "display_name"]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Other Info'), {'fields': ('display_name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
    )


admin.site.register(models.Author, UserAdmin)