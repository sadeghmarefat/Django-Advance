from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from blog.models import Post

User = get_user_model()

class PostTest(TestCase):
    def setUp(self):
        # ساخت کاربر تستی (با فرض اینکه مدل یوزر شما با ایمیل یا فیلدهای استاندارد کار می‌کند)
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')
        
        # ساخت پست تستی با محتوا برای تست متدهای مختلف
        self.post1 = Post.objects.create(
            title='Post 1', 
            content='Testing content snippet', 
            status=True, 
            author=self.user
        )

    def test_post_str(self):
        # تست متد __str__ که عنوان پست را برمی‌گرداند
        self.assertEqual(str(self.post1), 'Post 1')

    def test_post_get_snippet(self):
        # تست متد get_snippet که ۵ کاراکتر اول محتوا را برمی‌گرداند ('Testi')
        self.assertEqual(self.post1.get_snippet(), 'Testi')

    def test_post_get_absolute_api_url(self):
        # تست متد get_absolute_api_url که در مدل واقعی خود تعریف کرده‌اید
        expected_url = reverse("blog:api-v1:post-detail", kwargs={"pk": self.post1.pk})
        self.assertEqual(self.post1.get_absolute_api_url(), expected_url)