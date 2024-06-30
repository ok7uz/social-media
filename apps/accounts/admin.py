from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.accounts.models import User, Follow


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'created_at')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('username',)
    filter_horizontal = ('interests',)
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'profile_picture')}),
        ('Extra information', {'fields': ('password', 'last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'profile_picture', 'password1', 'password2'),
        }),
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
