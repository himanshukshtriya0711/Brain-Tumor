from django.contrib import admin
from .models import UserModel, BrainTumorAssessment, UserMedicalInfo

@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    exclude = ['password', 'last_login', 'groups', 'permissions', 'user_permissions', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['date_joined']

admin.site.register(BrainTumorAssessment)
admin.site.register(UserMedicalInfo)
