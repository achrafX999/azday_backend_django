from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from base.serializers import AddCategoryView
from .views import AddBusinessView, CategoryListView, GoogleLogin, RegisterUserView, sign_in_api  # Import de la vue GoogleLogin
from . import views 


urlpatterns = [
    #path('api/register/', views.register_api, name='register_api'),  
    path('api/auth/social/google/', GoogleLogin.as_view(), name='google_login'),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/login/', sign_in_api, name='login'),
    path('api/business/add/', AddBusinessView.as_view(), name='add_business'),
    path('api/category/add/', AddCategoryView.as_view(), name='add_category'),
    path('api/categories/', CategoryListView.as_view(), name='list_categories'),
    ]



# Only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


