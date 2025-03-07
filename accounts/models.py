from django.db import models
from django.contrib.auth.models import User

class UserModel(User):
    phone = models.CharField(max_length=15, blank=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

class BrainTumorAssessment(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    result = models.CharField(max_length=255, default="Pending")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class UserMedicalInfo(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    symptoms = models.TextField()
    duration = models.IntegerField()
    conditions = models.TextField(blank=True, null=True)
    conditions_image = models.ImageField(upload_to='conditions_images/', blank=True, null=True)
    previous_diagnosis = models.TextField(blank=True, null=True)
    diagnosis_image = models.ImageField(upload_to='diagnosis_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Medical Info"
    
