from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('email', 'first_name', 'is_staff', 'is_active', 'is_superuser')
        
    fieldsets = (
        ('authentication', {'fields': ('email', 'first_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('group permissions', {'fields': ('groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
        
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)