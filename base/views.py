# Imports Django
import traceback
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Imports DRF
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

# Imports tiers
import random
import json
from twilio.rest import Client

# Imports locaux
from .models import Business, BusinessImage, Category, Review, OpeningHours, CustomUser
from .forms import CustomUserCreationForm, BusinessForm
from .serializers import (
    CategorySerializer,
    UserSerializer,
    UserRegistrationSerializer,
    BusinessSerializer
)
from django.core.paginator import Paginator
from rest_framework.generics import RetrieveAPIView


@api_view(['POST'])
def register_api(request):
    data = request.data
    phone_number = data.get("phone_number")  # Récupérer le numéro de téléphone

    serializer = UserSerializer(data=data)
    
    if serializer.is_valid():
        user = serializer.save()
        if phone_number:  # Vérifier si un numéro de téléphone a été fourni
            user.phone_number = phone_number
            user.save()  # Sauvegarde en base de données

        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def sign_in_api(request):
    print("Données reçues :", request.data)  # 🔍 Vérifier les données dans le terminal Django

    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Récupérer l'utilisateur basé sur l'email
    User = get_user_model()
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

    # Vérifier le mot de passe
    if not user.check_password(password):
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

    # Générer un token d'authentification
    token, created = Token.objects.get_or_create(user=user)

    return Response({
        "message": "Login successful",
        "token": token.key,
        "user": UserSerializer(user).data  # Retourne les infos de l'utilisateur
    }, status=status.HTTP_200_OK)

class RegisterUserView(APIView):
    def post(self, request):
        print("----- Début de la méthode post -----")
        print("Données reçues :", request.data)

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            # Retirer le champ confirmPassword s'il existe
            data.pop('confirmPassword', None)

            email = data['email']
            password = data['password']
            first_name = data['first_name']
            last_name = data['last_name']
            phone_number = data['phone_number']

            if CustomUser.objects.filter(email=email).exists():
                print("Utilisateur déjà existant pour l'email :", email)
                return Response(
                    {'error': 'User with this email already exists.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                # Création de l'utilisateur
                user = CustomUser.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number
                )
                print("Utilisateur créé :", user)
            except Exception as e:
                print("Erreur lors de la création de l'utilisateur :", e)
                traceback.print_exc()
                return Response(
                    {'error': f'Error creating user: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Génération d'un code de vérification à 6 chiffres
            code = str(random.randint(100000, 999999))
            expires_at = timezone.now() + timezone.timedelta(minutes=10)
            user.verification_code = code
            user.code_expires_at = expires_at
            user.is_phone_verified = False

            try:
                user.save()
                print("Utilisateur sauvegardé avec succès.")
            except Exception as e:
                print("Erreur lors de la sauvegarde de l'utilisateur :", e)
                traceback.print_exc()
                return Response(
                    {'error': f'Error saving user: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Bloc d'envoi de SMS COMMENTÉ pour le test
            """
            try:
                account_sid = "YOUR_TWILIO_SID"
                auth_token = "YOUR_TWILIO_AUTH_TOKEN"
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                    body=f"Votre code de vérification est : {code}",
                    from_="+1234567890",  # Remplacez par votre numéro Twilio
                    to=phone_number
                )
            except Exception as e:
                print("Erreur lors de l'envoi du SMS :", e)
                traceback.print_exc()
                user.delete()
                return Response(
                    {'error': 'Failed to send SMS. Please try again later.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            """

            print("----- Fin de la méthode post -----")
            return Response(
                {'message': 'User created (SMS sending skipped for test).'},
                status=status.HTTP_201_CREATED
            )
        else:
            print("Erreur de validation du serializer :", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BusinessSearchView(APIView):
    def get(self, request):
        # Récupérer les paramètres de recherche
        category = request.query_params.get('category', '')
        city = request.query_params.get('city', '')
        page = request.query_params.get('page', 1)

        # Filtrer les entreprises
        businesses = Business.objects.all()
        if category:
            businesses = businesses.filter(category__name__icontains=category)
        if city:
            businesses = businesses.filter(address__icontains=city)

        # Mise en place de la pagination (10 résultats par page)
        paginator = Paginator(businesses, 10)
        try:
            businesses_page = paginator.page(page)
        except Exception as e:
            return Response({"error": "Page invalide."}, status=status.HTTP_400_BAD_REQUEST)

        # Sérialiser les résultats
        serializer = BusinessSerializer(businesses_page, many=True)
        data = {
            "results": serializer.data,
            "page": int(page),
            "total_pages": paginator.num_pages,
            "total_results": paginator.count,
        }
        return Response(data, status=status.HTTP_200_OK)
    
class BusinessDetailView(RetrieveAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    
class BusinessHelpfulView(APIView):
    def post(self, request, pk):
        try:
            business = Business.objects.get(pk=pk)
            business.helpful_count += 1
            business.save()
            return Response({'helpful_count': business.helpful_count}, status=status.HTTP_200_OK)
        except Business.DoesNotExist:
            return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)

class BusinessReportView(APIView):
    def post(self, request, pk):
        try:
            business = Business.objects.get(pk=pk)
            business.report_count += 1
            business.save()
            return Response({'report_count': business.report_count}, status=status.HTTP_200_OK)
        except Business.DoesNotExist:
            return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)
from .serializers import BusinessSerializer

class AddBusinessView(APIView):
    def post(self, request):
        # Valider les données du business via le serializer
        serializer = BusinessSerializer(data=request.data)
        if serializer.is_valid():
            # Créer le business en associant le propriétaire (request.user)
            business = serializer.save(owner=request.user)
            
            # Traitement des horaires d'ouverture
            opening_hours_data = request.data.get('opening_hours')
            if opening_hours_data:
                try:
                    # On attend que ce soit une liste d'objets, par exemple :
                    # [{"dayName": "Monday", "openTime": "08:00", "closeTime": "18:00"}, ...]
                    hours = json.loads(opening_hours_data)
                    for entry in hours:
                        day_name = entry.get('dayName')
                        open_time = entry.get('openTime')
                        close_time = entry.get('closeTime')
                        if day_name and open_time and close_time:
                            OpeningHours.objects.create(
                                business=business,
                                day=day_name,
                                open_time=open_time,
                                close_time=close_time
                            )
                        else:
                            return Response(
                                {'error': 'Each opening hours entry must include dayName, openTime and closeTime.'},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                except json.JSONDecodeError:
                    return Response(
                        {'error': 'Invalid JSON format for opening_hours.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except Exception as e:
                    return Response(
                        {'error': f'Error processing opening_hours: {str(e)}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                for key, file in request.FILES.items():
                    if key.startswith('images_'):
                        BusinessImage.objects.create(business=business, image=file)
            return Response(BusinessSerializer(business).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('search', None)
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)
        return queryset


from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
# Create your views here.


def home(request):
    businesses = Business.objects.all()
    context = {'businesses': businesses}
    return render(request,'base/index.html',context)


def business_profile(request, business_id):
    # Fetch the business details based on the ID
    business = get_object_or_404(Business, id=business_id)
    # Fetch reviews for the business (if a Review model exists)
    reviews = Review.objects.filter(business=business).order_by('-created_at')
    # Context to pass data to the template
    context = {
        'business': business,
        'reviews': reviews,
    }
    return render(request, 'base/business_detail.html', context)


def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a 'home' page after login
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'base/signin.html')






def logoutuser(request):
    logout(request)
    return redirect('home')



@login_required(login_url='login')
def business_create_view(request):
    if request.method == "POST":
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()
            return redirect('home')  # Redirect to a list view or success page
    else:
        form = BusinessForm()

    return render(request, 'base/business_form.html', {'form': form})

