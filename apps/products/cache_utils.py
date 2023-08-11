from django.core.cache import cache
from .models import Product

def get_cached_products():
    products = cache.get('cached_products')
    if products is None:
        products = list(Product.objects.all())
        cache.set('cached_products', products)
    return products

def invalidate_cached_products():
    cache.delete('cached_products')