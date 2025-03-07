from django.db import models
from django.contrib.auth.models import User

class UserModel(User):
    phone = models.CharField(max_length=15, blank=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.email

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()
    photo = models.ImageField(upload_to='doctor_photos/', default='doctor_photos/default.png')
    qualification = models.CharField(max_length=200)
    description = models.TextField()
    available_days = models.CharField(max_length=100)  # Store as comma-separated days
    available_times = models.CharField(max_length=100)  # Store as comma-separated time slots
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ]
    
    patient = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.patient.email} - Dr. {self.doctor.name} - {self.date}"

class Prescription(models.Model):
    patient = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    diagnosis = models.TextField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.email} - {self.date}"

class Medicine(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='medicines')
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.prescription.patient.email}"

class BrainTumorAssessment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]
    
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    scan_image = models.ImageField(upload_to='brain_scans/')
    result = models.CharField(max_length=255, default="Pending")
    confidence = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - Scan {self.id}"

    class Meta:
        ordering = ['-created_at']

class UserMedicalInfo(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]
    
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    symptoms = models.TextField()
    duration = models.IntegerField(help_text="Duration of symptoms in months")
    conditions = models.TextField(blank=True, null=True)
    conditions_image = models.ImageField(upload_to='conditions_images/', blank=True, null=True)
    previous_diagnosis = models.TextField(blank=True, null=True)
    diagnosis_image = models.ImageField(upload_to='diagnosis_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - Medical Info"
    
    class Meta:
        verbose_name_plural = "User Medical Information"
