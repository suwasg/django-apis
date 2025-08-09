import uuid 
from django.utils.text import slugify 

def generate_unique_slug(model_class, field_value):
    """
    Generate a unique slug for a model instance based on a field value.
    If the slug already exists, append a random UUID to make it unique.
    """
    slug = slugify(field_value)
    unique_slug = slug
    num = 1  # Counter to append if slug is not unique
    # Check if the slug already exists in the model
    while model_class.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{uuid.uuid4().hex[:8]}"  # Append a short UUID to ensure uniqueness
        # unique_slug = f"{slug}-{num}"
    return unique_slug
