from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model  # <--- این را اضافه کنید
from blog.models import Post

User = get_user_model()  # <--- به جای ایمپورت مستقیم User، از این استفاده کنید

class BaseTestCase(TestCase):
    def setUp(self):
        # این متد حالا به طور خودکار مدل کاربر سفارشی شما را می‌سازد
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')
        
        self.post1 = Post.objects.create(title='Post 1', status=True, author=self.user)
        self.post2 = Post.objects.create(title='Post 2', status=True, author=self.user)
        self.post3 = Post.objects.create(title='Post 3', status=True, author=self.user)

class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('blog:cbv_index'))
        self.assertEqual(response.status_code, 200)

class PostListViewTest(BaseTestCase):
    def test_post_list_view(self):
        # لاگین کردن کاربر چون ویو LoginRequiredMixin دارد
        self.client.force_login(self.user)
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        # بررسی تعداد آیتم‌های صفحه اول با توجه به paginate_by = 2
        self.assertEqual(len(response.context['page_obj']), 2)

class PostDetailViewTest(BaseTestCase):
    def test_post_detail_view(self):
        self.client.force_login(self.user)
        # استفاده از id پستی که در setUp ساختیم
        response = self.client.get(reverse('blog:post-detail', args=[self.post1.pk]))
        self.assertEqual(response.status_code, 200)

class ContactViewTest(BaseTestCase):
    def test_contact_view_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('blog:contact'))
        self.assertEqual(response.status_code, 200)

    def test_contact_view_post(self):
        self.client.force_login(self.user)
        # ارسال داده‌های معتبر برای فرم تماس
        response = self.client.post(reverse('blog:contact'), {
            'name': 'Test Name',
            'message': 'Test Message'
        })
        # بعد از موفقیت فرم معمولاً ریدایرکت (302) اتفاق می‌افتد
        self.assertEqual(response.status_code, 302)

class CreatePostViewTest(BaseTestCase):
    def test_create_post_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('blog:create-post'))
        self.assertEqual(response.status_code, 200)

class PostEditViewTest(BaseTestCase):
    def test_edit_post_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('blog:edit-post', args=[self.post1.pk]))
        self.assertEqual(response.status_code, 200)

class PostDeleteViewTest(BaseTestCase):
    def test_delete_post_view(self):
        self.client.force_login(self.user)
        # معمولاً برای حذف درخواست POST فرستاده می‌شود
        response = self.client.post(reverse('blog:delete-post', args=[self.post1.pk]))
        self.assertEqual(response.status_code, 302) # ریدایرکت بعد از حذف موفق