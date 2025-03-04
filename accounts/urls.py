from django.urls import path
from .views import signup, user_login,dashboard  # Import login view

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),  # Add login URL
    path('dashboard/', dashboard, name='dashboard'),  # Add dashboard URL
]
