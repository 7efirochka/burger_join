from . import views
from django.urls import path

app_name = 'base_menu'

urlpatterns = [
    path('', views.menu_view, name='menu'),
    path('profile/', views.profile_view, name="profile"),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.cart_add, name='cart_add'),
    path('cart/change/', views.cart_change, name='cart_change'),
    path('cart/remove/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]