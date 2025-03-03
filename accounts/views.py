from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from .models import UserModel
from django.shortcuts import render
from django.contrib import messages

def home(request):
    return render(request, 'accounts/home.html')  # Create this template



def user_login(request):
    return render(request, 'accounts/login.html')  # Create this template


def signup(request):
    if request.method == "POST":
        print(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2', '')  # Optional field
        state = request.POST.get('state')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'accounts/signup.html')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, 'accounts/signup.html')

        # Save user to the database
        user = UserModel(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address1=address1,
            address2=address2,
            state=state,
            country=country,
            zip_code=zip_code,
            email=email,
            password=make_password(password),  # Hash password before saving
        )
        user.save()

        messages.success(request, "Signup successful! You can now log in.")
        return redirect('login')

    return render(request, 'accounts/signup.html')
