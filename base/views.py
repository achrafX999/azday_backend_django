from django.contrib.auth import authenticate, login , logout
from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib import messages
from rest_framework import status  # ✅ Import ajouté

from .models import Business , Review
from .forms import CustomUserCreationForm , BusinessForm 
from django.contrib.auth.decorators import login_required

###########################CETTE PARTIE POUR API JSON FAIT PAR ACHRAF
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer

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
