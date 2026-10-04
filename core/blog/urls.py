from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='cbv_index'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('go-to-index/', views.RedirectToIndex.as_view(), name='go-to-index'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('create/', views.CreatePostView.as_view(), name='create-post'),
    path('posts/<int:pk>/edit', views.PostEditView.as_view(), name='edit-post'),

    path('posts/<int:pk>/delete', views.PostDeleteView.as_view(), name='delete-post'),
    path('api/v1/', include('blog.api.v1.urls'))
]
