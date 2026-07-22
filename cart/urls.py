from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart/', views.cart_page, name='cart'),
    path('cart/item/<int:item_id>/update/', views.update_cart_item, name='update_item'),
    path('cart/item/<int:item_id>/remove/', views.remove_cart_item, name='remove_item'),
    path('checkout/', views.checkout_page, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
]
