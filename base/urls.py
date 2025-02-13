from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views 


urlpatterns = [
    path('api/register/', views.register_api, name='register_api'),  # API REST pour Angular

    ]



# Only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


