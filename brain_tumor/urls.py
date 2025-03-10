from django.contrib import admin
from django.urls import path, include
from accounts.views import home  # Import home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', home, name='home'),
    path("", include("backend.urls")),
]
