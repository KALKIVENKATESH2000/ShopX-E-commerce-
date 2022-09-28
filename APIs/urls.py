from django.urls import path
from APIs.views import *

urlpatterns = [
    path('products/', ListProduct.as_view(), name='products'),
    path('products/<int:pk>/', DetailProduct.as_view(), name='product'),
    path('users/', ListUser.as_view(), name='users'),
    path('users/<int:pk>/', DetailUser.as_view(), name='user'),
    path('cart/', ListCart.as_view(), name='carts'),
    path('cart/<int:pk>/', DetailCart.as_view(), name='cart'),
    path('orders/', ListOrder.as_view(), name='orders'),
    path('orders/<int:pk>/', DetailOrder.as_view(), name='order'),
]
