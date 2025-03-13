from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from base.serializers import AddCategoryView
from .views import AddBusinessView, CategoryListView, GoogleLogin, RegisterUserView, sign_in_api , VisiteurCreateView # Import de la vue GoogleLogin
from .views import AddBusinessView, BusinessHelpfulView, BusinessListView, BusinessReportView, BusinessSearchView,BusinessDetailView, CategoryListView, GoogleLogin, RegisterUserView, sign_in_api  # Import de la vue GoogleLogin
from .views import ReviewListView, ReviewDetailView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView
from . import views 


urlpatterns = [
    #path('api/register/', views.register_api, name='register_api'),  
    path('api/auth/social/google/', GoogleLogin.as_view(), name='google_login'),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/login/', sign_in_api, name='login'),
    path('api/business/add/', AddBusinessView.as_view(), name='add_business'),
    path('api/category/add/', AddCategoryView.as_view(), name='add_category'),
    path('api/categories/', CategoryListView.as_view(), name='list_categories'),
    path('api/visiteur/', VisiteurCreateView.as_view(), name='visiteur-create'),
    path('api/search/', BusinessSearchView.as_view(), name='business-search'),
    path('api/business/<int:pk>/', BusinessDetailView.as_view(), name='business-detail'),
    path('api/business/<int:pk>/helpful/', BusinessHelpfulView.as_view(), name='business-helpful'),
    path('api/business/<int:pk>/report/', BusinessReportView.as_view(), name='business-report'),
    path('api/business/all/', BusinessListView.as_view(), name='business-all'),    
    path('api/reviews/', ReviewListView.as_view(), name='review-list'),
    path('api/reviews/create/', ReviewCreateView.as_view(), name='review-create'),
    ]



# Only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


