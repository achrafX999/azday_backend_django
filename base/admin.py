from django.contrib import admin
from .models import CustomUser, Category, Business, BusinessImage, Review, OpeningHours , Visiteur

# Enregistrer le modèle CustomUser si vous utilisez un admin personnalisé
admin.site.register(CustomUser)

# Enregistrer les autres modèles
admin.site.register(Category)
admin.site.register(Business)
admin.site.register(BusinessImage)
admin.site.register(Review)
admin.site.register(OpeningHours)
admin.site.register(Visiteur)
