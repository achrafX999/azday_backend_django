from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import AddBusinessView, GoogleLogin, RegisterUserView  # Import de la vue GoogleLogin
from . import views 


urlpatterns = [
    #path('api/register/', views.register_api, name='register_api'),  
    path('api/auth/social/google/', GoogleLogin.as_view(), name='google_login'),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/business/add/', AddBusinessView.as_view(), name='add_business'),

    ]



# Only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


