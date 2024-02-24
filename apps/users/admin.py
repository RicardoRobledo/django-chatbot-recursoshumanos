from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):

    list_display = ('username', 'name', 'email', 'is_superuser')
    readonly_fields = ('is_superuser', 'is_active')
    search_fields = ('username', 'name', 'email')

    fieldsets = (
        (None, {'fields': ('name', 'username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'username', 'email', 'password1', 'password2')}
        ),
    )


admin.site.register(User, CustomUserAdmin)
