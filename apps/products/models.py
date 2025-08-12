from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone

from common.utils import generate_unique_slug, generate_uuid
# Create your models here.
USER = settings.AUTH_USER_MODEL

class Category(models.Model):
    """Product Category Model wiht Parent-child relationship.
    Represents a product category with support for:
    - Parent-child hierarchy (e.g., Electronics → Mobiles → Smartphones)
    - SEO metadata
    - Optional image (icon/banner)
    - Active/inactive state for soft-hiding categories"""
    name = models.CharField(max_length=100, unique=True)
    # Unique slug for URL-friendly identifiers (e.g., "electronics")
    # Blank=True so it can be auto-generated if not provided
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True, help_text="Category banner or icon")
    # Self-referencing foreign key to create subcategories
    # related_name='children' allows easy access to subcategories
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    # Whether category is active or hidden from public
    is_active = models.BooleanField(default=True)
    # SEO metadata fields
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    # Auto timestamps for creation and last update
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Proper plural name for django admin interfaces
        verbose_name_plural = 'Categories'
        # default ordering/sorting alphabetically by name
        ordering = ['name']
        # Database indexes to speed up queries
        indexes = [
            models.Index(fields = ['slug']), # for fast lookups by slug on URLs
            models.Index(fields = ['created_at']), # for sorting by creation date
            models.Index(fields = ['name']), # for fast lookups/search by name
            models.Index(fields = ['is_active']), # for filtering active categories
        ]
    
    def __str__(self):
        """
        String representation for admin panel and shell.
        Returns the category name.
        """
        return self.name
    
    def save(self, *args, **kwargs):
        """
        Override save method to auto-generate slug if not provided.
        Uses a helper function `generate_unique_slug` to ensure uniqueness.
        """
        if not self.slug:
            self.slug = generate_unique_slug(Category, self.name, slug_field='slug')
            super().save(*args, **kwargs)
    def get_absolute_url(self):
        """
        Returns the URL for this category instance.
        Uses Django's reverse function to generate URL based on slug.
        Returns the canonical URL for this category detail page.
        Useful in templates for linking directly to a category.
        """
        return reverse('category_detail', kwargs={'slug': self.slug})
    
class Tag(models.Model):
    """Product Tag Model.
    Represents a tag that can be associated with products.
    Tags are used for categorization and filtering products."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Tags'
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        """String representation for admin panel and shell."""
        return self.name
    
    def save(self, *args, **kwargs):
        """Override save method to auto-generate slug if not provided.
        Uses a helper function `generate_unique_slug` to ensure uniqueness."""
        if not self.slug:
            self.slug = generate_unique_slug(Tag, self.name, slug_field='slug')
        super().save(*args, **kwargs)

class Product(models.Model):
    """Product Model.
    Represents a product with:
    - Name, description, price, stock quantity
    - Category and tags for organization
    - SEO metadata
    - Image upload support
    - Timestamps for creation and last update"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    # Foreign key to Category model for product categorization
    # related_name='products' allows easy access to products in a category
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')

    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    # SEO metadata fields
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    # Auto timestamps for creation and last update
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
            models.Index(fields=['name']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        """String representation for admin panel and shell."""
        return self.name
    
    def save(self, *args, **kwargs):
        """Override save method to auto-generate slug if not provided.
        Uses a helper function `generate_unique_slug` to ensure uniqueness."""
        if not self.slug:
            self.slug = generate_unique_slug(Product, self.name, slug_field='slug')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Returns the URL for this product instance.
        Uses Django's reverse function to generate URL based on slug."""
        return reverse('product_detail', kwargs={'slug': self.slug})