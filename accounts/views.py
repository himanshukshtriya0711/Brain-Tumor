from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from .models import UserModel, BrainTumorAssessment, UserMedicalInfo, Doctor, Appointment, Prescription
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def home(request):
    return render(request, 'accounts/home.html')  

@ensure_csrf_cookie
def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                messages.success(request, "Successfully logged in!")
                return redirect('dashboard')
        except User.DoesNotExist:
            pass
        
        messages.error(request, "Invalid email or password")
    return render(request, 'accounts/login.html')

@login_required
def prescriptions_view(request):
    prescriptions = Prescription.objects.filter(
        patient=request.user.usermodel
    ).order_by('-date')
    return render(request, 'accounts/prescriptions.html', {'prescriptions': prescriptions})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('login')

@ensure_csrf_cookie
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
            username=email,
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
            # Check file size (10MB limit)
            if scan_image.size > 10 * 1024 * 1024:
                messages.error(request, "File size must be less than 10MB")
                return redirect('upload_scan')
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if scan_image.content_type not in allowed_types:
                messages.error(request, "Please upload a valid image file (JPG, PNG, or GIF)")
                return redirect('upload_scan')
            
            try:
                assessment = BrainTumorAssessment.objects.create(
                    user=request.user.usermodel,
                    scan_image=scan_image,
                    status='pending'
                )
                messages.success(request, "Scan uploaded successfully! Processing...")
                return redirect('view_results')
            except Exception as e:
                messages.error(request, "An error occurred while uploading your scan. Please try again.")
                return redirect('upload_scan')
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

@login_required
def appointments(request):
    upcoming_appointments = Appointment.objects.filter(
        patient=request.user.usermodel,
        date__gte=timezone.now().date()
    ).order_by('date', 'time')
    
    doctors = Doctor.objects.all().order_by('-experience')
    
    return render(request, 'accounts/appointments.html', {
        'upcoming_appointments': upcoming_appointments,
        'doctors': doctors
    })

@login_required
def book_appointment(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        reason = request.POST.get('reason')
        
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            time = datetime.strptime(time_str, '%H:%M').time()
            
            # Check if appointment slot is available
            existing_appointment = Appointment.objects.filter(
                doctor=doctor,
                date=date,
                time=time,
                status__in=['pending', 'confirmed']
            ).exists()
            
            if existing_appointment:
                messages.error(request, 'This time slot is already booked. Please choose another time.')
                return redirect('appointments')
            
            # Create new appointment
            Appointment.objects.create(
                patient=request.user.usermodel,
                doctor=doctor,
                date=date,
                time=time,
                reason=reason,
                status='pending'
            )
            
            messages.success(request, 'Appointment booked successfully! We will confirm it shortly.')
        except (Doctor.DoesNotExist, ValueError) as e:
            messages.error(request, 'Invalid appointment details. Please try again.')
        
    return redirect('appointments')

@login_required
def cancel_appointment(request, appointment_id):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.usermodel)
        if appointment.status in ['pending', 'confirmed']:
            appointment.status = 'cancelled'
            appointment.save()
            messages.success(request, 'Appointment cancelled successfully.')
        else:
            messages.error(request, 'Cannot cancel this appointment.')
    
    return redirect('appointments')


from django.shortcuts import render
from django.core.files.storage import default_storage
from django.http import JsonResponse, FileResponse
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from .utils.model_utils import load_detection_model, preprocess_image, predict_tumor

model = load_detection_model()

def process_scan(request):
    if request.method == 'POST' and request.FILES.get('scan'):
        scan = request.FILES['scan']
        if scan.name.split('.')[-1].lower() not in ['jpg', 'jpeg']:
            return JsonResponse({'error': 'Only JPG and JPEG files are allowed'}, status=400)

        scan_path = default_storage.save('uploads/' + scan.name, scan)
        full_scan_path = os.path.join(default_storage.location, scan_path)

        img_array = preprocess_image(full_scan_path)
        label, confidence = predict_tumor(model, img_array)

        request.session['scan_result'] = {
            'filename': scan.name,
            'label': label,
            'confidence': round(confidence, 2),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def view_results(request):
    result = request.session.get('scan_result', {})
    return render(request, 'accounts/view_results.html', {'result': result})

def download_pdf(request):
    result = request.session.get('scan_result', {})
    if not result:
        return JsonResponse({'error': 'No scan result found'}, status=400)

    pdf_path = os.path.join(default_storage.location, 'reports', f"{result['filename']}_report.pdf")
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 750, "Brain Tumor Detection Report")
    c.drawString(100, 730, f"Scan Name: {result['filename']}")
    c.drawString(100, 710, f"Prediction: {result['label']}")
    c.drawString(100, 690, f"Confidence: {result['confidence']}%")
    c.drawString(100, 670, f"Date & Time: {result['timestamp']}")

    if result['confidence'] > 40:
        story = "This result indicates a significant chance of tumor presence. We strongly recommend consulting a specialist for further diagnosis and medical support. Remember, early detection can save lives."
    else:
        story = "The scan suggests no strong evidence of tumor at this time, but regular checkups are always a good practice to maintain health. Stay cautious and take care."

    c.drawString(100, 650, "Note:")
    text_object = c.beginText(100, 630)
    text_object.setTextOrigin(100, 630)
    text_object.setFont("Helvetica", 10)
    for line in story.split('. '):
        text_object.textLine(line.strip())
    c.drawText(text_object)

    c.save()

    return FileResponse(open(pdf_path, 'rb'), as_attachment=True, filename=f"{result['filename']}_report.pdf")

