from django.urls import path
from . import views
urlpatterns = [
    path('cart/', views.cart_detail, name='cart-detail'),
    path('cart/add/', views.add_to_cart, name='cart-add'),
    path('cart/item/<int:item_id>/', views.cart_item_detail, name='cart-item-detail'),
]
