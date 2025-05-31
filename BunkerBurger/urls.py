from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
import sys
import os

# Fix Python module path to make 'main' importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include main app URLs for registration and home page
    path('', include('main.urls')),
    path('menu/', include('base_menu.urls'), name="menu"),
    path('accounts/', include('django.contrib.auth.urls')),
    # Note: Registration URL is already included in main.urls
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)