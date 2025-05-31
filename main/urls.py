# urls.py (в основном каталоге проекта)
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.view, name='main'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name = "register"),
    # path('accounts/login/', views.login, name="login")
]
