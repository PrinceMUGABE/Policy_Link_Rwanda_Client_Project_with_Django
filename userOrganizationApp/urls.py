from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_user_institution, name='create_user_institution'),
    path('<int:pk>/', views.get_user_institution_by_id, name='get_user_institution_by_id'),
    path('delete/<int:pk>/', views.delete_user_institution, name='delete_user_institution'),
]
