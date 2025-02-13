from django.contrib import admin

# Register your models here.

from .models import CustomUser , Business , Review , OpeningHours
admin.site.register(CustomUser)
admin.site.register(Business)
admin.site.register(Review)
admin.site.register(OpeningHours)