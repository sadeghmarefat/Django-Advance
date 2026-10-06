from django.urls import path, include
from . import views
from rest_framework import routers


app_name = 'api-v1'

router = routers.DefaultRouter()
router.register('post', views.PostModelViewSet, basename='post')
router.register('category', views.CategoryModelViewSet, basename='category')
urlpatterns = router.urls



# urlpatterns = [
#     path('post/', views.PostList.as_view() , name='post-list'),
#     path('post/<int:pk>/', views.PostDetail.as_view(), name= 'post-detail'),
#
# ]