from django.urls import path
from .views import signup, user_login,user_medi_info,dashboard # Import login view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),  # Add login URL
    path('user_medi_info/', user_medi_info, name='user_medi_info'),  # Add user_medi_info URL
    path('dashboard/', dashboard, name='dashboard'),  # Add dashboard URL
    
    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
