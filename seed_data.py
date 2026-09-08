import os
import django
import urllib.request
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Category, Product

electronics, _ = Category.objects.get_or_create(name='Electronics', slug='electronics')
fashion, _ = Category.objects.get_or_create(name='Fashion', slug='fashion')

items = [
    {
        'name': 'Wireless Noise-Canceling Headphones',
        'slug': 'wireless-headphones',
        'description': 'High-fidelity audio with active noise cancellation and 30-hour battery life.',
        'price': 99.99,
        'stock': 25,
        'category': electronics,
        'img_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&q=80',
        'file_name': 'headphones.jpg'
    },
    {
        'name': 'Smart Fitness Watch',
        'slug': 'smart-fitness-watch',
        'description': 'Track heart rate, workouts, sleep, and receive notifications with water resistance.',
        'price': 49.99,
        'stock': 40,
        'category': electronics,
        'img_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&q=80',
        'file_name': 'watch.jpg'
    },
    {
        'name': 'Classic Cotton Hoodie',
        'slug': 'classic-cotton-hoodie',
        'description': 'Comfortable, breathable all-season hoodie crafted with 100%% premium organic cotton.',
        'price': 39.99,
        'stock': 50,
        'category': fashion,
        'img_url': 'https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=600&q=80',
        'file_name': 'hoodie.jpg'
    },
    {
        'name': 'Minimalist Leather Backpack',
        'slug': 'minimalist-leather-backpack',
        'description': 'Durable, waterproof everyday backpack with dedicated padded laptop compartment.',
        'price': 59.99,
        'stock': 15,
        'category': fashion,
        'img_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&q=80',
        'file_name': 'backpack.jpg'
    },
]

headers = {'User-Agent': 'Mozilla/5.0'}
for item in items:
    p, created = Product.objects.get_or_create(
        slug=item['slug'],
        defaults={
            'name': item['name'],
            'description': item['description'],
            'price': item['price'],
            'stock': item['stock'],
            'category': item['category'],
        }
    )
    if not p.image:
        try:
            req = urllib.request.Request(item['img_url'], headers=headers)
            with urllib.request.urlopen(req) as resp:
                p.image.save(item['file_name'], ContentFile(resp.read()), save=True)
            print(f"Attached image for {p.name}")
        except Exception as e:
            print(f"Failed to fetch image for {p.name}: {e}")

print("Products updated with images successfully!")
