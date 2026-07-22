from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Category, Product, WishlistItem, StockAlert
from .serializers import CategorySerializer, ProductSerializer, WishlistItemSerializer, StockAlertSerializer


def get_or_create_cart(request):
    from cart.models import Cart
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    if not request.session.session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key, user=None)
    return cart


def home(request):
    category_slug = request.GET.get('category')
    q = request.GET.get('q', '')
    sort_by = request.GET.get('sort_by', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    min_rating = request.GET.get('min_rating', '')
    tag_filter = request.GET.get('tag_filter', '')
    in_stock = request.GET.get('in_stock', '')
    deals_only = request.GET.get('deals_only', '')

    products = Product.objects.filter(is_active=True).select_related('category')
    if category_slug and category_slug != 'all':
        products = products.filter(category__slug=category_slug)
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    if min_rating:
        try:
            products = products.filter(rating__gte=float(min_rating))
        except ValueError:
            pass
    if tag_filter:
        products = products.filter(tag=tag_filter)
    if in_stock:
        products = products.filter(stock__gt=0)
    if deals_only:
        products = products.filter(original_price__isnull=False)

    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    elif sort_by == 'best_seller':
        products = products.filter(tag='best_seller').order_by('-review_count')
    else:
        products = products.order_by('-created_at')

    categories = Category.objects.annotate(product_count=Count('products')).all()
    cart = get_or_create_cart(request)
    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = list(request.user.wishlist_items.values_list('product_id', flat=True))
    return render(request, 'catalog/home.html', {
        'products': products[:24],
        'categories': categories,
        'active_category': category_slug or 'all',
        'query': q,
        'cart': cart,
        'wishlist_ids': wishlist_ids,
        'sort_by': sort_by,
        'min_price': min_price,
        'max_price': max_price,
        'min_rating': min_rating,
        'tag_filter': tag_filter,
        'in_stock': in_stock,
        'deals_only': deals_only,
        'total_products': Product.objects.filter(is_active=True).count(),
    })


def categories_page(request):
    categories = Category.objects.annotate(product_count=Count('products'))
    return render(request, 'catalog/categories.html', {'categories': categories})


def deals(request):
    products = Product.objects.filter(
        is_active=True, original_price__isnull=False
    ).select_related('category')
    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = list(request.user.wishlist_items.values_list('product_id', flat=True))
    return render(request, 'catalog/deals.html', {'products': products, 'deals_count': products.count(), 'wishlist_ids': wishlist_ids})


def blog(request):
    posts = [
        {
            'title': 'Why Mechanical Keyboards Boost Productivity',
            'date': 'June 15, 2026',
            'excerpt': 'Discover how tactile switches and customizable layouts can improve your typing speed and comfort during long sessions.',
            'slug': 'mechanical-keyboards-productivity',
            'read_time': '5 min read',
        },
        {
            'title': 'Building the Ultimate Remote Work Setup',
            'date': 'May 28, 2026',
            'excerpt': 'From ergonomic chairs to ultra-wide monitors, we break down the essential gear for a productive remote workspace.',
            'slug': 'ultimate-remote-work-setup',
            'read_time': '8 min read',
        },
        {
            'title': 'Noise Cancelling Headphones for Deep Focus',
            'date': 'May 10, 2026',
            'excerpt': 'How premium noise cancellation technology helps professionals enter flow state and maintain concentration for hours.',
            'slug': 'noise-cancelling-deep-focus',
            'read_time': '4 min read',
        },
        {
            'title': 'The Best USB-C Docking Stations in 2026',
            'date': 'April 22, 2026',
            'excerpt': 'A comprehensive comparison of docking stations that transform your laptop into a full workstation.',
            'slug': 'best-usb-c-docking-stations',
            'read_time': '6 min read',
        },
    ]
    return render(request, 'catalog/blog.html', {'posts': posts})


def about(request):
    return render(request, 'catalog/about.html')


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related('category'), slug=slug, is_active=True)
    related = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:3]
    complementary = Product.objects.filter(
        is_active=True
    ).exclude(pk=product.pk).exclude(category=product.category)[:2]
    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = list(request.user.wishlist_items.values_list('product_id', flat=True))
    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'related_products': related,
        'complementary_products': complementary,
        'wishlist_ids': wishlist_ids,
    })


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['price', 'created_at']


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wishlist_list(request):
    items = WishlistItem.objects.filter(user=request.user).select_related('product', 'product__category')
    serializer = WishlistItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def wishlist_toggle(request):
    product_id = request.data.get('product_id')
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.delete()
        return Response({'status': 'removed', 'product_id': product_id})
    return Response({'status': 'added', 'product_id': product_id}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def wishlist_sync(request):
    product_ids = request.data.get('product_ids', [])
    added = 0
    for pid in product_ids:
        try:
            product = Product.objects.get(pk=pid, is_active=True)
            _, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
            if created:
                added += 1
        except Product.DoesNotExist:
            continue
    return Response({'added': added})


@api_view(['POST'])
def stock_alert_create(request):
    product_id = request.data.get('product')
    email = request.data.get('email')
    if not product_id or not email:
        return Response({'detail': 'Product and email are required.'}, status=status.HTTP_400_BAD_REQUEST)
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    alert, created = StockAlert.objects.get_or_create(product=product, email=email.strip())
    return Response(
        {'status': 'subscribed' if created else 'already_subscribed', 'detail': 'We will notify you when this product is back in stock.'},
        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
    )
