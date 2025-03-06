from django.db import models
from django.contrib.auth.hashers import make_password

class UserModel(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, unique=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Store hashed password later

    def __str__(self):
        return self.email

from django.db import models
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password

# Custom User Model
class User(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only hash password if the user is new
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    


from django.db import models

class BrainTumorAssessment(models.Model):
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
        return f"Assessment - {self.age} years old ({self.gender})"


