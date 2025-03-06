from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from .models import UserModel
from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse


def home(request):
    return render(request, 'accounts/home.html')  # Create this template



def user_login(request):
    return render(request, 'accounts/login.html')  # Create this template

def user_medi_info(request):
    return render(request, 'accounts/user_medi_info.html')  # Create this template


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
        return redirect('user_medi_info')

    return render(request, 'accounts/signup.html')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')  # Create this template   


def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                return redirect('dashboard')  # Redirect to dashboard if authentication succeeds
            else:
                return JsonResponse({'error': 'Not a user'}, status=400)  # Throw error if password is incorrect
        except User.DoesNotExist:
            return JsonResponse({'error': 'Not a user'}, status=400)  # Throw error if user does not exist
    return render(request, 'signup.html')  # Render login page for GET requests

from django.shortcuts import render, redirect
from .models import BrainTumorAssessment

def assessment_form(request):
    if request.method == "POST":
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        symptoms = ", ".join(request.POST.getlist("symptoms"))
        duration = request.POST.get("duration")
        conditions = request.POST.get("conditions")
        conditions_image = request.FILES.get("conditions_image")
        previous_diagnosis = request.POST.get("previous_diagnosis")
        diagnosis_image = request.FILES.get("diagnosis_image")

        BrainTumorAssessment.objects.create(
            age=age,
            gender=gender,
            symptoms=symptoms,
            duration=duration,
            conditions=conditions,
            conditions_image=conditions_image,
            previous_diagnosis=previous_diagnosis,
            diagnosis_image=diagnosis_image,
        )

        return redirect("dashboard")

    return render(request, "assessment_form.html")

def dashboard(request):
    assessments = BrainTumorAssessment.objects.all()
    return render(request, "dashboard.html", {"assessments": assessments})
