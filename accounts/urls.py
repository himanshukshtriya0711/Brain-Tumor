from django.urls import path
from .views import (
    signup, user_login, user_medi_info, dashboard,
    personal_info, diagnostics, upload_scan, view_results,
    logout_view
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('personal-info/', personal_info, name='personal_info'),
    path('diagnostics/', diagnostics, name='diagnostics'),
    path('upload-scan/', upload_scan, name='upload_scan'),
    path('view-results/', view_results, name='view_results'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
