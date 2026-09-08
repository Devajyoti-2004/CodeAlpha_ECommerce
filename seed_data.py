import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Category, Product

electronics, _ = Category.objects.get_or_create(name='Electronics', slug='electronics')
fashion, _ = Category.objects.get_or_create(name='Fashion', slug='fashion')

products = [
    {'title': 'Wireless Noise-Canceling Headphones', 'slug': 'wireless-headphones', 'description': 'High-fidelity audio with active noise cancellation and 30-hour battery life.', 'price': 99.99, 'stock': 25, 'category': electronics},
    {'title': 'Smart Fitness Watch', 'slug': 'smart-fitness-watch', 'description': 'Track heart rate, workouts, sleep, and receive notifications with water resistance.', 'price': 49.99, 'stock': 40, 'category': electronics},
    {'title': 'Classic Cotton Hoodie', 'slug': 'classic-cotton-hoodie', 'description': 'Comfortable, breathable all-season hoodie crafted with 100%% premium organic cotton.', 'price': 39.99, 'stock': 50, 'category': fashion},
    {'title': 'Minimalist Leather Backpack', 'slug': 'minimalist-leather-backpack', 'description': 'Durable, waterproof everyday backpack with dedicated padded laptop compartment.', 'price': 59.99, 'stock': 15, 'category': fashion},
]

for item in products:
    Product.objects.get_or_create(slug=item['slug'], defaults=item)

print("Database seeded successfully with sample products!")
