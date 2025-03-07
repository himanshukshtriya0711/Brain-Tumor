from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from .models import UserModel, BrainTumorAssessment, UserMedicalInfo    
from django.contrib import messages
from django.http import JsonResponse

def home(request):
    return render(request, 'accounts/home.html')  

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password")
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('login')

def signup(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2', '')  
        state = request.POST.get('state')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'accounts/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, 'accounts/signup.html')

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
            password=make_password(password),  
        )
        user.save()

        messages.success(request, "Signup successful! You can now log in.")
        return redirect('user_medi_info')

    return render(request, 'accounts/signup.html')

@login_required
def dashboard(request):
    user = request.user
    assessments = BrainTumorAssessment.objects.filter(user=user).order_by('-created_at')[:5]
    context = {
        "assessments": assessments,
        "user": user
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def personal_info(request):
    user = request.user
    medical_info = UserMedicalInfo.objects.filter(user=user).first()
    
    if request.method == "POST":
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        
        messages.success(request, "Personal information updated successfully!")
        return redirect('personal_info')
        
    context = {
        "user": user,
        "medical_info": medical_info
    }
    return render(request, 'accounts/personal_info.html', context)

@login_required
def diagnostics(request):
    user = request.user
    assessments = BrainTumorAssessment.objects.filter(user=user).order_by('-created_at')
    context = {
        "assessments": assessments
    }
    return render(request, 'accounts/diagnostics.html', context)

@login_required
def upload_scan(request):
    if request.method == "POST":
        scan_image = request.FILES.get('scan_image')
        if scan_image:
            assessment = BrainTumorAssessment.objects.create(
                user=request.user,
                scan_image=scan_image,
                status='pending'
            )
            messages.success(request, "Scan uploaded successfully! Processing...")
            return redirect('view_results')
        else:
            messages.error(request, "Please select a scan image to upload.")
    
    return render(request, 'accounts/upload_scan.html')

@login_required
def view_results(request):
    user = request.user
    assessments = BrainTumorAssessment.objects.filter(user=user).order_by('-created_at')
    context = {
        "assessments": assessments
    }
    return render(request, 'accounts/view_results.html', context)

@login_required
def user_medi_info(request):
    if request.method == "POST":
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        symptoms = ", ".join(request.POST.getlist("symptoms"))
        duration = request.POST.get("duration")
        conditions = request.POST.get("conditions")
        conditions_image = request.FILES.get("conditions_image")
        previous_diagnosis = request.POST.get("previous_diagnosis")
        diagnosis_image = request.FILES.get("diagnosis_image")

        user = UserModel.objects.get(id=request.user.id)

        UserMedicalInfo.objects.create(
            user=user,
            age=age,
            gender=gender,
            symptoms=symptoms,
            duration=duration,
            conditions=conditions,
            conditions_image=conditions_image,
            previous_diagnosis=previous_diagnosis,
            diagnosis_image=diagnosis_image,
        )

        messages.success(request, "Medical information saved successfully!")

        return redirect("dashboard")  

    return render(request, "accounts/user_medi_info.html")
