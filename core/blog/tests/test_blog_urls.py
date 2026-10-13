from django.test import TestCase
from django.urls import resolve, reverse
from .. import views as blog
# Create your tests here.

class UrlTest(TestCase):
    def test_urls(self):
        url = reverse('blog:cbv_index')
        self.assertEqual(resolve(url).func.view_class, blog.IndexView)
        url = reverse('blog:post_list')
        self.assertEqual(resolve(url).func.view_class, blog.PostListView)
        url = reverse('blog:go-to-index')
        self.assertEqual(resolve(url).func.view_class, blog.RedirectToIndex)
        url = reverse('blog:post-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, blog.PostDetailView)
        url = reverse('blog:contact')
        self.assertEqual(resolve(url).func.view_class, blog.ContactView)
        url = reverse('blog:create-post')
        self.assertEqual(resolve(url).func.view_class, blog.CreatePostView)
        url = reverse('blog:edit-post', args=[1])
        self.assertEqual(resolve(url).func.view_class, blog.PostEditView)
        url = reverse('blog:delete-post', args=[1])
        self.assertEqual(resolve(url).func.view_class, blog.PostDeleteView)