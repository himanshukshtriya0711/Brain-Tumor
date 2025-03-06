from django.urls import path
from .views import signup, user_login,user_medi_info # Import login view

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),  # Add login URL
    path('user_medi_info/', user_medi_info, name='user_medi_info'),  # Add user_medi_info URL
]
