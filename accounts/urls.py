from django.urls import path
from .views import (
    signup, user_login, user_medi_info, dashboard,
    personal_info, diagnostics, upload_scan, view_results,
    logout_view, appointments, book_appointment, cancel_appointment,prescriptions_view
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
    path('appointments/', appointments, name='appointments'),
    path('appointments/book/', book_appointment, name='book_appointment'),
    path('appointments/<int:appointment_id>/cancel/', cancel_appointment, name='cancel_appointment'),
    path('prescriptions/', prescriptions_view, name='prescriptions'),
    path('user-medi-info/', user_medi_info, name='user_medi_info'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from .views import process_scan, view_results, download_pdf

urlpatterns += [
    path('process_scan/', process_scan, name='process_scan'),
    path('view_results/', view_results, name='view_results'),
    path('download_pdf/', download_pdf, name='download_pdf'),
]
