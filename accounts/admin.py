from django.contrib import admin
from .models import UserModel, User, BrainTumorAssessment

admin.site.register(UserModel)

admin.site.register(BrainTumorAssessment)