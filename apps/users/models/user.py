from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class  CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a regular User with the given email and password.
        """
        if not email:
            raise ValueError("User must have an email address.")
        email = self.normalize_email(email) # Normalize the email by lowercasing the domain part of the email.
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # Hashes the password.
        user.save(using=self._db)  # save to the correct database.
        # user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        # validating superuser flags.
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email instead of username.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField(null= True, blank= True)
    # profile_image = models.URLField(null=True, blank=True) # cloudinary
    profile_image = models.ImageField(upload_to='media/profile_images', null=True, blank=True) # local
    
    # Permissions & status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Timestamps
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # Link Manager
    objects = CustomUserManager()

    # Tell Django which field is used to log in
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.email
    

class UserSettings(models.Model):
    """
    Model to store user settings/preferences.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    receive_emails = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)
    show_email_publicly = models.BooleanField(default=False)
    show_phone_number_publicly = models.BooleanField(default=False)
    show_date_of_birth_publicly = models.BooleanField(default=False)
    show_profile_image_publicly = models.BooleanField(default=False)
    show_full_name_publicly = models.BooleanField(default=False)
    show_last_login = models.BooleanField(default=False)
    show_date_joined = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings for {self.user.first_name}"

