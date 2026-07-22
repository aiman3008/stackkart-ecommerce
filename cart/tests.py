import pytest
from catalog.models import Category, Product
from cart.models import Cart, CartItem

@pytest.mark.django_db
def test_cart_total():
    cat = Category.objects.create(name='Phones')
    product = Product.objects.create(category=cat, name='DevPhone', description='Phone', price=100000, stock=3)
    cart = Cart.objects.create(session_key='abc')
    CartItem.objects.create(cart=cart, product=product, quantity=2)
    assert cart.total == 200000
