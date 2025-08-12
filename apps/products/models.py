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
    
