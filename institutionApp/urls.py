from django.urls import path
from . import views
from .views import download_policies_pdf, get_comment_by_id

urlpatterns = [
    path('view_all_institutions/', views.view_all_institutions, name='view_all_institutions'),
    path('add_institution/', views.add_institution, name='add_institution'),
    path('delete_institution/<int:institution_id>', views.delete_institution, name='delete_institution'),
    path('view_all_departments/', views.view_all_departments, name='view_all_departments'),
    path('view_all_policies/', views.view_all_policies, name='view_all_policies'),
    path('get_institutions_by_type/', views.get_institutions_by_type, name='get_institutions_by_type'),
    path('get_departments_by_institution/<int:institution_id>/', views.get_departments_by_institution, name='get_departments_by_institution'),
    path('get_policies_by_department/', views.get_policies_by_department, name='get_policies_by_department'),
    path('get_policies_by_department_id/<int:department_id>/', views.get_policies_by_department_by_id, name='get_policies_by_department_id'),
    path('get_policy_by_id/<int:policy_id>/', views.get_policy_by_id, name='get_policy_by_id'),
    
    # reports
    path('total_institutions/', views.total_institutions, name='total_institutions'),
    path('institutions_distribution/', views.institutions_distribution, name='institutions_distribution'),
    path('all_institutions/', views.all_institutions, name='all_institutions'),
    path('average_departments_per_institution/', views.average_departments_per_institution, name='average_departments_per_institution'),
    path('download_policies_pdf/<str:institution_name>/<str:department_name>/', download_policies_pdf, name='download_policies_pdf'),
    path('increase_over_time/', views.institution_increase_over_time, name='institution_increase_over_time'),
    
    
    # comments
    path('add_comment/<int:policy_id>', views.add_comment, name='add_comment'),
    path('view_all_comments/', views.view_all_comments, name='view_all_comments'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('search_comment/', views.search_comment, name='search_comment'),
    path('comment/<int:comment_id>/', get_comment_by_id, name='get_comment_by_id'),
    
    #comment reports
    path('comment_reports/', views.generate_comment_reports, name='generate_comment_reports'),
    
    
    path('download_all_policies_pdf/', views.download_all_policies_pdf, name='download_all_policies_pdf'),
    path('download_all_policies_excel/', views.download_all_policies_excel, name='download_all_policies_excel'),
    path('download_all_institutions_pdf/', views.download_all_institutions_pdf, name='download_all_institutions_pdf'),
    path('download_all_institutions_excel/', views.download_all_institutions_excel, name='download_all_institutions_excel'),
    path('download_all_departments_pdf/', views.download_all_departments_pdf, name='download_all_departments_pdf'),
    path('download_all_departments_excel/', views.download_all_departments_excel, name='download_all_departments_excel'),
    path('comment_reply/', views.comment_reply, name='comment_reply'),
    path('get_comment_by_username/<str:username>/', views.get_comments_by_username, name='get_comment_by_username'),
    
    
    path('download_policies_by_department_pdf/<int:department_id>/', views.download_policies_by_department_pdf, name='download_policies_by_department_pdf'),
    path('comment_replies/<str:email>/', views.get_comment_replies, name='get_comment_replies'),
]
