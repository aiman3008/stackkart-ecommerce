from rest_framework import serializers
from .models import Category, Product, WishlistItem, StockAlert

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'parent']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(source='category', queryset=Category.objects.all(), write_only=True)
    discount_percent = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'subtitle', 'description', 'price',
            'original_price', 'stock', 'image_url', 'rating', 'review_count',
            'tag', 'discount_percent', 'is_active', 'category', 'category_id',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug']

class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = WishlistItem
        fields = ['id', 'product', 'created_at']

class StockAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockAlert
        fields = ['id', 'product', 'email', 'created_at', 'notified']
        read_only_fields = ['created_at', 'notified']
