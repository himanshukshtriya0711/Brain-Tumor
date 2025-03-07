import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brain_tumor.settings')
django.setup()

from accounts.models import Doctor

# Create a sample doctor
doctor = Doctor.objects.create(
    name="Sarah Johnson",
    specialization="Neurologist",
    experience=15,
    qualification="MD, PhD in Neurology",
    description="Dr. Sarah Johnson is a board-certified neurologist with over 15 years of experience in diagnosing and treating brain tumors. She specializes in advanced imaging techniques and personalized treatment plans.",
    available_days="Monday, Wednesday, Friday",
    available_times="09:00-12:00, 14:00-17:00"
)

print(f"Created doctor: {doctor}")
