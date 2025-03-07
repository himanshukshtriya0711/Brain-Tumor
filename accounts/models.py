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
