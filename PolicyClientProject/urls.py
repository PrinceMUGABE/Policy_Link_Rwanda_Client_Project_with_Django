
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('userAccount.urls')),
    path('institution/', include('institutionApp.urls')),
    path('userOrganization', include('userOrganizationApp.urls')),
 
]
