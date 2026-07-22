import pytest
from catalog.models import Category, Product

@pytest.mark.django_db
def test_product_slug_is_generated():
    cat = Category.objects.create(name='Laptops')
    product = Product.objects.create(category=cat, name='DevBook Pro', description='Fast laptop', price=250000, stock=5)
    assert product.slug == 'devbook-pro'
