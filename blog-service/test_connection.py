#!/usr/bin/env python
"""
Script para verificar la conexión de todos los componentes del Blog Service.
"""
import os
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_service.settings')

import django
django.setup()

from django.db import connection
from django.core.cache import cache
from categories.models import Category
from authors.models import Author
from posts.models import Post

def test_database():
    """Verificar conexión a PostgreSQL."""
    print("🔍 Testing Database Connection...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ Database connected: {version[:50]}...")
            return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_redis():
    """Verificar conexión a Redis."""
    print("\n🔍 Testing Redis Connection...")
    try:
        cache.set('test_key', 'test_value', 10)
        value = cache.get('test_key')
        if value == 'test_value':
            print("✅ Redis connected and working")
            return True
        else:
            print("❌ Redis not returning correct values")
            return False
    except Exception as e:
        print(f"❌ Redis error: {e}")
        return False

def test_models():
    """Verificar que los modelos estén funcionando."""
    print("\n🔍 Testing Models...")
    try:
        categories_count = Category.objects.count()
        authors_count = Author.objects.count()
        posts_count = Post.objects.count()
        published_count = Post.objects.filter(status='published').count()
        
        print(f"✅ Models working:")
        print(f"   - Categories: {categories_count}")
        print(f"   - Authors: {authors_count}")
        print(f"   - Posts: {posts_count} (Published: {published_count})")
        return True
    except Exception as e:
        print(f"❌ Models error: {e}")
        return False

def main():
    """Ejecutar todas las pruebas."""
    print("="*60)
    print("   BLOG SERVICE - CONNECTION TEST")
    print("="*60)
    
    db_ok = test_database()
    redis_ok = test_redis()
    models_ok = test_models()
    
    print("\n" + "="*60)
    if db_ok and redis_ok and models_ok:
        print("✅ ALL TESTS PASSED - Blog Service is ready!")
        print("="*60)
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED - Check the errors above")
        print("="*60)
        sys.exit(1)

if __name__ == '__main__':
    main()
