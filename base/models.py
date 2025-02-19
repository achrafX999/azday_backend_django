from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from base.managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # Utilisation de l'email comme identifiant unique
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, blank=True, null=True)  

    is_active = models.BooleanField(default=True)  # Utile pour activer/désactiver des comptes
    is_staff = models.BooleanField(default=False)  # Utile pour les accès admin

    USERNAME_FIELD = 'email'  # Authentification avec email uniquement
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Champs obligatoires lors de l'inscription

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Business(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='businesses')
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)  # e.g., Coiffeur, Plumber, etc.
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='business_images/', blank=True, null=True)  # Photo de l'entreprise
    latitude = models.FloatField()  # Pour la localisation sur la carte
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating de 1 à 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.email} for {self.business.name}"


class OpeningHours(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='opening_hours')
    day = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ])
    open_time = models.TimeField()
    close_time = models.TimeField()

    def __str__(self):
        return f"{self.business.name} - {self.day}"
