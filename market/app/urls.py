from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('catalog/', catalog, name='catalog'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('cart/', cart_view, name='cart'),
    path('cart/update/<int:pk>/', update_cart, name='update_cart'),
    path('cart/remove/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', clear_cart, name='clear_cart'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add_to_cart'),


]
