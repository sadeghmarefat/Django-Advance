import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from blog.models import Post, Category

User = get_user_model()


@pytest.mark.django_db
class TestPostAPI:
    """Test cases for Blog Post API endpoints."""

    def setup_method(self):
        """Set up test client and user."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Test Category')
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='This is a test post content.',
            status=True,
            category=self.category
        )


    def test_get_post_list_unauthenticated(self):
        """Test GET request to post list endpoint without authentication."""
        response = self.client.get('/blog/api/v1/post/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_post_list_authenticated(self):
        """Test GET request to post list endpoint with authentication."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/blog/api/v1/post/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == 'Test Post'

    def test_get_post_detail_unauthenticated(self):
        """Test GET request to post detail endpoint without authentication."""
        response = self.client.get(f'/blog/api/v1/post/{self.post.pk}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_post_detail_authenticated(self):
        """Test GET request to post detail endpoint with authentication."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/blog/api/v1/post/{self.post.pk}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Test Post'
        assert response.data['content'] == 'This is a test post content.'

    def test_get_post_list_empty(self):
        """Test GET request when no published posts exist."""
        self.post.status = False
        self.post.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/blog/api/v1/post/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 0

    def test_get_post_list_multiple_posts(self):
        """Test GET request with multiple published posts."""
        Post.objects.create(
            author=self.user,
            title='Second Post',
            content='Second post content.',
            status=True,
            category=self.category
        )
        Post.objects.create(
            author=self.user,
            title='Third Post',
            content='Third post content.',
            status=True,
            category=self.category
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/blog/api/v1/post/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3

    def test_create_post_unauthenticated(self):
        """Test POST request to create post without authentication."""
        post_data = {
            'title': 'New Post',
            'content': 'New post content.',
            'status': True,
            'category': self.category.id
        }
        response = self.client.post('/blog/api/v1/post/', post_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_post_authenticated(self):
        """Test POST request to create post with authentication."""
        post_data = {
            'title': 'New Post',
            'content': 'New post content.',
            'status': True,
            'category': self.category.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/blog/api/v1/post/', post_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Post'
        assert response.data['author'] == 'Test'
        assert Post.objects.count() == 2
