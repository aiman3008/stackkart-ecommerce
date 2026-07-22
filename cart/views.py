from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from catalog.models import Product
from orders.services import create_order_from_cart
from payments.models import PaymentRecord
from .forms import CheckoutForm
from .models import Cart, CartItem
from .serializers import CartSerializer


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    if not request.session.session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key, user=None)
    return cart


def cart_page(request):
    cart = get_or_create_cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})


def update_cart_item(request, item_id):
    if request.method != 'POST':
        return redirect('cart:cart')
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    quantity = max(1, int(request.POST.get('quantity', item.quantity)))
    if quantity > item.product.stock:
        messages.error(request, f'Only {item.product.stock} items available for {item.product.name}.')
    else:
        item.quantity = quantity
        item.save(update_fields=['quantity'])
        messages.success(request, 'Cart updated.')
    return redirect('cart:cart')


def remove_cart_item(request, item_id):
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        CartItem.objects.filter(id=item_id, cart=cart).delete()
        messages.success(request, 'Item removed from cart.')
    return redirect('cart:cart')


@login_required
def checkout_page(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty. Add products before checkout.')
        return redirect('cart:cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            shipping_address = (
                f"Name: {form.cleaned_data['full_name']}\n"
                f"Phone: {form.cleaned_data['phone']}\n"
                f"City: {form.cleaned_data['city']}\n"
                f"Address: {form.cleaned_data['address']}"
            )
            payment_method = form.cleaned_data['payment_method']
            try:
                with transaction.atomic():
                    order = create_order_from_cart(request.user, cart, shipping_address=shipping_address)
                    payment_status = PaymentRecord.Status.INITIATED
                    reference_prefix = 'COD'
                    if payment_method == 'jazzcash':
                        reference_prefix = 'JC-DEMO'
                    elif payment_method == 'easypaisa':
                        reference_prefix = 'EP-DEMO'
                    PaymentRecord.objects.create(
                        order=order,
                        gateway=payment_method,
                        gateway_reference=f'{reference_prefix}-{order.id}',
                        amount=order.total,
                        status=payment_status,
                    )
                return redirect('cart:order_success', order_id=order.id)
            except ValueError as exc:
                messages.error(request, str(exc))
    else:
        initial = {
            'full_name': request.user.get_full_name() or request.user.username,
            'payment_method': 'cod',
        }
        form = CheckoutForm(initial=initial)

    return render(request, 'cart/checkout.html', {'cart': cart, 'form': form})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(request.user.orders.prefetch_related('payments'), id=order_id)
    payment = order.payments.first()
    return render(request, 'cart/order_success.html', {'order': order, 'payment': payment})


@api_view(['GET'])
def cart_detail(request):
    cart = get_or_create_cart(request)
    return Response(CartSerializer(cart).data)


@api_view(['POST'])
@transaction.atomic
def add_to_cart(request):
    cart = get_or_create_cart(request)
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))
    product = Product.objects.select_for_update().get(pk=product_id, is_active=True)
    if quantity < 1:
        return Response({'detail': 'Quantity must be at least 1.'}, status=status.HTTP_400_BAD_REQUEST)
    if product.stock < quantity:
        return Response({'detail': 'Not enough stock.'}, status=status.HTTP_400_BAD_REQUEST)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})
    if not created:
        new_quantity = item.quantity + quantity
        if new_quantity > product.stock:
            return Response({'detail': 'Not enough stock.'}, status=status.HTTP_400_BAD_REQUEST)
        item.quantity = new_quantity
        item.save(update_fields=['quantity'])
    return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


@api_view(['PATCH', 'DELETE'])
def cart_item_detail(request, item_id):
    cart = get_or_create_cart(request)
    item = CartItem.objects.get(pk=item_id, cart=cart)
    if request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    quantity = int(request.data.get('quantity', item.quantity))
    if quantity < 1:
        return Response({'detail': 'Quantity must be at least 1.'}, status=status.HTTP_400_BAD_REQUEST)
    item.quantity = quantity
    item.save(update_fields=['quantity'])
    return Response(CartSerializer(cart).data)
