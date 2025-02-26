from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from base.managers import CustomUserManager

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from base.managers import CustomUserManager
from django.utils import timezone

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Champs pour la vérification par SMS
    is_phone_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    code_expires_at = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)  # Activer/désactiver des comptes
    is_staff = models.BooleanField(default=False)  # Pour l'accès admin

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def is_code_valid(self, code):
        """Vérifie que le code fourni correspond et n'est pas expiré."""
        if self.verification_code == code and self.code_expires_at and timezone.now() < self.code_expires_at:
            return True
        return False




# ------------------------------
# Modèle Business
# ------------------------------
from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Chaque catégorie est unique

    def __str__(self):
        return self.name

class Business(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='businesses')
    name = models.CharField(max_length=255)  # Correspond à "businessName" du formulaire Angular
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='business_images/', blank=True, null=True)
    latitude = models.FloatField()   # Pour afficher la position sur la carte (obligatoire)
    longitude = models.FloatField()  # Pour afficher la position sur la carte (obligatoire)
    
    # Champs JSON pour stocker plusieurs valeurs sous forme de liste
    languages = models.JSONField(blank=True, null=True)
    payment_methods = models.JSONField(blank=True, null=True)
    product_services = models.JSONField(blank=True, null=True)
    specialize = models.JSONField(blank=True, null=True)
    
    # Champs supplémentaires pour l'admin
    helpful_count = models.PositiveIntegerField(default=0)
    report_count = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    response_rate = models.FloatField(default=0.0)
    active = models.BooleanField(default=True)
    banned = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# ------------------------------
# Modèle pour plusieurs Images supplémentaires associées à un Business
# ------------------------------
class BusinessImage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='business_images/')

    def __str__(self):
        return f"Image for {self.business.name}"

# ------------------------------
# Modèle pour les Avis sur un Business
# ------------------------------
class Review(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Note de 1 à 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.email} for {self.business.name}"

# ------------------------------
# Modèle pour les Horaires d'Ouverture d'un Business
# ------------------------------
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
