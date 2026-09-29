from typing import Any

from django.contrib import admin
from .models import Post, Contact


# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    exclude = ['author']
    list_display = ('title', 'get_author_name', 'status', 'published_at')
    list_filter = ('status', 'published_at')
    search_fields = ('title', 'content')

    @admin.display(description='author', ordering='author__first_name')
    def get_author_name(self, obj):
        return obj.author.first_name if obj.author.first_name else obj.author.email

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'message')
    list_filter = ('name',)
    search_fields = ('name',)