from django.db import transaction
from .models import Order, OrderItem

@transaction.atomic
def create_order_from_cart(user, cart, shipping_address=''):
    order = Order.objects.create(user=user, total=cart.total, shipping_address=shipping_address)
    for item in cart.items.select_related('product').select_for_update():
        product = item.product
        if product.stock < item.quantity:
            raise ValueError(f'Not enough stock for {product.name}')
        product.stock -= item.quantity
        product.save(update_fields=['stock'])
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item.quantity,
            unit_price=product.price,
        )
    cart.items.all().delete()
    return order
