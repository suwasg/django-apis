import uuid 
from django.utils.text import slugify 

def generate_unique_slug(model_class, field_value, slug_field="slug", max_length=250):
    """
    Generate a unique slug for a model instance based on a field value.
    Uses short UUIDs for uniqueness when needed.
    """
    base_slug = slugify(field_value)[:max_length]  # truncate base
    slug = base_slug
    while model_class.objects.filter(**{slug_field: slug}).exists():
        suffix = uuid.uuid4().hex[:8]
        # Ensure final slug length stays within limit
        slug = f"{base_slug[:max_length - len(suffix) - 1]}-{suffix}"
    return slug

def generate_uuid():
    """
    Generate a random UUID.
    """
    return uuid.uuid4().hex  # Returns a random UUID as a string
    # return str(uuid.uuid4())  # Returns a random UUID as a string
