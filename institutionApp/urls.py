from django.urls import path
from . import views
from .views import download_policies_pdf

urlpatterns = [
    path('view_all_institutions/', views.view_all_institutions, name='view_all_institutions'),
    path('add_institution/', views.add_institution, name='add_institution'),
    path('delete_institution/<int:institution_id>/', views.delete_institution, name='delete_institution'),
    path('view_all_departments/', views.view_all_departments, name='view_all_departments'),
    path('view_all_policies/', views.view_all_policies, name='view_all_policies'),
    path('get_institutions_by_type/', views.get_institutions_by_type, name='get_institutions_by_type'),
    path('get_departments_by_institution/', views.get_departments_by_institution, name='get_departments_by_institution'),
    path('get_policies_by_department/', views.get_policies_by_department, name='get_policies_by_department'),
    
    # reports
    path('total_institutions/', views.total_institutions, name='total_institutions'),
    path('institutions_distribution/', views.institutions_distribution, name='institutions_distribution'),
    path('all_institutions/', views.all_institutions, name='all_institutions'),
    path('average_departments_per_institution/', views.average_departments_per_institution, name='average_departments_per_institution'),
    path('download_policies_pdf/<str:institution_name>/<str:department_name>/', download_policies_pdf, name='download_policies_pdf'),
    path('increase_over_time/', views.institution_increase_over_time, name='institution_increase_over_time'),
    
    
    # comments
    path('add_comment/', views.add_comment, name='add_comment'),
    path('view_all_comments/', views.view_all_comments, name='view_all_comments'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('search_comment/', views.search_comment, name='search_comment'),
    
    #comment reports
    path('comment_reports/', views.generate_comment_reports, name='generate_comment_reports'),
]
