from django.contrib import admin
from .models import Profile, User
from django.contrib.auth.admin import UserAdmin

# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "is_staff", "is_active", "is_superuser", "is_verified")
    list_filter = ("email", "is_staff", "is_active", "is_superuser", "is_verified")

    fieldsets = (
        ("authentication", {"fields": ("email", "first_name", "password")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "is_superuser", "is_verified")},
        ),
        ("group permissions", {"fields": ("groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "is_verified",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(Profile)
