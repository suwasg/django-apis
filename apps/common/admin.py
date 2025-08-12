from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Product
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Columns to display in the category list view in the admin
    list_display = ('name', 'parent', 'is_active', 'created_at', 'updated_at', 'image_preview')
    
    # Filters shown in the sidebar for easy filtering of categories
    list_filter = ('is_active', 'created_at', 'updated_at', 'parent')
    
    # Fields searchable by text in the search box on top
    search_fields = ('name', 'slug', 'description')
    
    # Default ordering of categories in the list view (alphabetical by name)
    ordering = ('name',)
    
    # Auto-fill the slug field from the name field when creating/editing
    prepopulated_fields = {'slug': ('name',)}
    
    # Fields that are read-only in the admin form
    readonly_fields = ('created_at', 'updated_at', 'slug')
    
    # Enable autocomplete dropdown for the parent category selection (useful for many categories)
    autocomplete_fields = ('parent',)
    
    # Number of categories to show per admin page
    list_per_page = 6

    def image_preview(self, obj):
        """
        Display a small preview thumbnail of the category image in the list view.
        Shows a placeholder '-' if no image is set.
        """
        if obj.image:
            return format_html(
                '<img src="{}" style="width:40px; height:40px; object-fit:cover; border-radius:4px;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Image"  # Column header name in the admin
    image_preview.allow_tags = True

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # Columns to show in tag list view
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    
    # Searchable fields for quick lookup
    search_fields = ('name',)
    
    # Auto-fill slug field from name in forms
    prepopulated_fields = {'slug': ('name',)}

    
