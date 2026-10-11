from .main import urlpatterns as main_urls
from .profile import urlpatterns as profile_urls

app_name = 'accounts-api-v1'

urlpatterns = main_urls + profile_urls

__all__ = ['urlpatterns', 'app_name']
