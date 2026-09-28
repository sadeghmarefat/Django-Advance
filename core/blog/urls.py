from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='cbv_index'),
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('go-to-index/', views.RedirectToIndex.as_view(), name='go-to-index'),
]
