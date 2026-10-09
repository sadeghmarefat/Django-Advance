from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Post(models.Model):
    '''Model representing a blog post.'''
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    status = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_snippet(self):
        return self.content[:5]

    def get_absolute_api_url(self):
        return reverse('blog:api-v1:post-detail', kwargs={'pk': self.pk})


class Category(models.Model):
    '''Model representing a blog post category.'''
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name

