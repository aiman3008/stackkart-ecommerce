from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet,
    wishlist_list, wishlist_toggle, wishlist_sync,
    stock_alert_create,
)

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('wishlist/', wishlist_list, name='wishlist-list'),
    path('wishlist/toggle/', wishlist_toggle, name='wishlist-toggle'),
    path('wishlist/sync/', wishlist_sync, name='wishlist-sync'),
    path('stock-alert/', stock_alert_create, name='stock-alert'),
]
