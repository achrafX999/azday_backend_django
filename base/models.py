from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from base.managers import CustomUserManager



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Champs pour la vérification par SMS, etc.
    is_phone_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    code_expires_at = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


from django.db import models
from django.conf import settings

# Modèle pour les catégories (par exemple, Coiffeur, Plombier, etc.)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Chaque catégorie est unique

    def __str__(self):
        return self.name

# Modèle principal Business
class Business(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='businesses')
    name = models.CharField(max_length=255)  # Correspond à "businessName" du formulaire Angular
    description = models.TextField(blank=True)
    
    # Utilisation d'une relation pour la catégorie afin de permettre une gestion via l'admin
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Adresse et contact
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # Image de profil (pour l'image principale du business)
    profile_picture = models.ImageField(upload_to='business_images/', blank=True, null=True)
    
    # Localisation géographique
    latitude = models.FloatField()   # Pour afficher la position sur la carte (obligatoire)
    longitude = models.FloatField()  # Pour afficher la position sur la carte (obligatoire)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Modèle pour stocker plusieurs images supplémentaires associées à un Business
class BusinessImage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='business_images/')

    def __str__(self):
        return f"Image for {self.business.name}"

# Modèle pour les avis sur un Business
class Review(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Note de 1 à 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.email} for {self.business.name}"

# Modèle pour les horaires d'ouverture d'un Business
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
