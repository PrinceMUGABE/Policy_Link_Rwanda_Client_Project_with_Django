from django.contrib import admin
from django.urls import path, include
# Remove the line below since it's causing the ImportError
# from . import account

# Correct the import statement for the app's views


urlpatterns = [
    path('admin/', admin.site.urls),
    # Use the correct URL pattern for including the app's URLs
    path('', include('account.urls')),
]
