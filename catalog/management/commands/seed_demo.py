from django.core.management.base import BaseCommand
from catalog.models import Category, Product

CATEGORIES = [
    ('Laptop Accessories', 'icon-laptop'),
    ('Keyboards', 'icon-keyboard'),
    ('Mice', 'icon-mouse'),
    ('Audio', 'icon-headphones'),
    ('Monitors', 'icon-monitor'),
    ('Smart Tech', 'icon-zap'),
]

PRODUCTS = [
    {
        'category': 'Keyboards',
        'name': 'Keychron K8 Pro',
        'subtitle': 'Wireless Mechanical Keyboard',
        'desc': 'Premium wireless mechanical keyboard with hot-swappable switches, RGB backlight, and Mac/Windows compatibility. Perfect for anyone who demands tactile precision.',
        'price': 99.99,
        'original_price': None,
        'stock': 45,
        'image': 'https://images.unsplash.com/photo-1595225476474-87563907a212?q=80&w=800&auto=format&fit=crop',
        'rating': 4.8,
        'reviews': 1200,
        'tag': 'best_seller',
    },
    {
        'category': 'Mice',
        'name': 'Logitech MX Master 3S',
        'subtitle': 'Performance Wireless Mouse',
        'desc': 'Ultra-fast tracking, ergonomic design, and silent clicks. The ultimate productivity mouse for professionals and creatives with multi-device support.',
        'price': 99.99,
        'original_price': None,
        'stock': 38,
        'image': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?q=80&w=800&auto=format&fit=crop',
        'rating': 4.7,
        'reviews': 982,
        'tag': 'new',
    },
    {
        'category': 'Audio',
        'name': 'Sony WH-1000XM5',
        'subtitle': 'Premium Noise Cancelling Headphones',
        'desc': 'Industry-leading noise cancellation with 30-hour battery life. Crystal-clear calls and immersive sound for deep focus during work and study sessions.',
        'price': 339.99,
        'original_price': 399.99,
        'stock': 22,
        'image': 'https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?q=80&w=800&auto=format&fit=crop',
        'rating': 4.8,
        'reviews': 1100,
        'tag': 'sale',
    },
    {
        'category': 'Laptop Accessories',
        'name': 'Nulaxy Laptop Stand',
        'subtitle': 'Ergonomic Aluminum Stand',
        'desc': 'Adjustable aluminum laptop stand for better posture and airflow. Compatible with all laptops up to 17 inches. Solid build with anti-slip pads.',
        'price': 39.99,
        'original_price': None,
        'stock': 85,
        'image': 'https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?q=80&w=800&auto=format&fit=crop',
        'rating': 4.6,
        'reviews': 850,
        'tag': 'popular',
    },
    {
        'category': 'Monitors',
        'name': 'LG UltraGear 27"',
        'subtitle': 'QHD IPS Gaming Monitor',
        'desc': '27-inch QHD IPS display with 144Hz refresh rate and 1ms response time. HDR10 support and AMD FreeSync for smooth visuals during work and play.',
        'price': 299.99,
        'original_price': 374.99,
        'stock': 15,
        'image': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?q=80&w=800&auto=format&fit=crop',
        'rating': 4.7,
        'reviews': 640,
        'tag': 'sale',
    },
    {
        'category': 'Laptop Accessories',
        'name': 'Anker 575 USB-C Dock',
        'subtitle': '13-in-1 Docking Station',
        'desc': 'Expand your laptop with triple display support, 100W Power Delivery, USB-C, USB-A, Ethernet, and SD card slots. Essential for any modern workstation.',
        'price': 149.99,
        'original_price': None,
        'stock': 30,
        'image': 'https://images.unsplash.com/photo-1625760483538-570bc912934c?q=80&w=800&auto=format&fit=crop',
        'rating': 4.5,
        'reviews': 420,
        'tag': 'new',
    },
    {
        'category': 'Audio',
        'name': 'Elgato Wave:3',
        'subtitle': 'USB Condenser Microphone',
        'desc': 'Professional USB microphone with proprietary anti-distortion technology. Perfect for streaming, podcasting, and crystal-clear video calls.',
        'price': 129.99,
        'original_price': None,
        'stock': 55,
        'image': 'https://images.unsplash.com/photo-1590602847861-f357a9332bbc?q=80&w=800&auto=format&fit=crop',
        'rating': 4.9,
        'reviews': 2100,
        'tag': 'best_seller',
    },
    {
        'category': 'Laptop Accessories',
        'name': 'Anker 737 Power Bank',
        'subtitle': '24,000mAh 140W Output',
        'desc': 'High-capacity power bank with smart digital display and 140W output. Charge your laptop, phone, and tablet simultaneously on the go.',
        'price': 89.99,
        'original_price': 99.99,
        'stock': 60,
        'image': 'https://images.unsplash.com/photo-1609091839313-d6805d1e4c20?q=80&w=800&auto=format&fit=crop',
        'rating': 4.6,
        'reviews': 780,
        'tag': 'sale',
    },
    {
        'category': 'Keyboards',
        'name': 'Keychron Q1 Pro',
        'subtitle': 'QMK/VIA Wireless Mechanical Keyboard',
        'desc': 'Full aluminum body with double-gasket design and hot-swappable switches. QMK/VIA programmable for ultimate customization.',
        'price': 199.99,
        'original_price': None,
        'stock': 18,
        'image': 'https://images.unsplash.com/photo-1587829741301-dc798b91add1?q=80&w=800&auto=format&fit=crop',
        'rating': 4.9,
        'reviews': 540,
        'tag': 'new',
    },
    {
        'category': 'Smart Tech',
        'name': 'Raspberry Pi 5',
        'subtitle': '8GB Single Board Computer',
        'desc': 'Next-generation single-board computer with 2.4GHz quad-core ARM Cortex-A76 CPU. Perfect for home automation, IoT projects, media centers, and learning.',
        'price': 79.99,
        'original_price': None,
        'stock': 12,
        'image': 'https://images.unsplash.com/photo-1631552726683-2e85c55f07b2?q=80&w=800&auto=format&fit=crop',
        'rating': 4.8,
        'reviews': 3200,
        'tag': 'popular',
    },
    {
        'category': 'Monitors',
        'name': 'Dell UltraSharp 32"',
        'subtitle': '4K USB-C Hub Monitor',
        'desc': 'Stunning 4K IPS display with 99% sRGB coverage. Built-in USB-C hub with 90W power delivery. Ideal for designers, creators, and professionals.',
        'price': 549.99,
        'original_price': 629.99,
        'stock': 8,
        'image': 'https://images.unsplash.com/photo-1547394765-185e1e68f34e?q=80&w=800&auto=format&fit=crop',
        'rating': 4.7,
        'reviews': 450,
        'tag': 'sale',
    },
    {
        'category': 'Mice',
        'name': 'Razer DeathAdder V3 Pro',
        'subtitle': 'Ultra-Lightweight Wireless Mouse',
        'desc': '63g ultra-lightweight design with Focus Pro 30K optical sensor. 90-hour battery life and HyperSpeed wireless technology.',
        'price': 149.99,
        'original_price': None,
        'stock': 25,
        'image': 'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?q=80&w=800&auto=format&fit=crop',
        'rating': 4.6,
        'reviews': 890,
        'tag': 'best_seller',
    },
]

class Command(BaseCommand):
    help = 'Seed demo categories and products for StackKart.'

    def handle(self, *args, **options):
        # Migrate legacy category
        old_cat = Category.objects.filter(name='Dev Tools').first()
        if old_cat:
            old_cat.name = 'Smart Tech'
            old_cat.icon = 'icon-zap'
            old_cat.save()
            self.stdout.write(self.style.WARNING('Renamed "Dev Tools" category to "Smart Tech".'))

        for cat_name, icon in CATEGORIES:
            Category.objects.get_or_create(name=cat_name, defaults={'icon': icon})

        for p in PRODUCTS:
            category = Category.objects.get(name=p['category'])
            Product.objects.update_or_create(
                name=p['name'],
                defaults={
                    'category': category,
                    'subtitle': p['subtitle'],
                    'description': p['desc'],
                    'price': p['price'],
                    'original_price': p['original_price'],
                    'stock': p['stock'],
                    'image_url': p['image'],
                    'rating': p['rating'],
                    'review_count': p['reviews'],
                    'tag': p['tag'],
                    'is_active': True,
                },
            )
        self.stdout.write(self.style.SUCCESS('Seeded StackKart demo products.'))
