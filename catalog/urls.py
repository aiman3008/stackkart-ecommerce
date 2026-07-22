from django.urls import path
from . import views

app_name = 'catalog'
urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.categories_page, name='categories'),
    path('deals/', views.deals, name='deals'),
    path('blog/', views.blog, name='blog'),
    path('about/', views.about, name='about'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
]
