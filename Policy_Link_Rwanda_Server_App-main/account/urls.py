
from django.urls import path
from . import views

urlpatterns = [

    path('api/view_all_institutions/', views.view_all_institutions, name='view_all_institutions_api'),
    path('api/add_institution/', views.add_institution, name='add_institution_api'),
    path('api/update_institution/', views.update_institution, name='update_institution_api'),
    path('api/delete_institution/', views.delete_institution, name='delete_institution_api'),


    path('api/view_all_departments/', views.view_all_departments, name='view_all_departments_api'),
    path('api/add_department/', views.add_department, name='add_department_api'),
    path('api/update_department/', views.update_department, name='update_department_api'),
    path('api/delete_department/', views.delete_department, name='delete_department_api'),



    path('api/view_all_policies/', views.view_all_policies, name='view_all_policies_api'),
    path('api/add_policy/', views.add_policy, name='add_policy_api'),
    path('api/update_policy/', views.update_policy, name='update_policy_api'),
    path('api/delete_policy/', views.delete_policy, name='delete_policy_api'),

    path('api/get_institutions_by_type/', views.get_institutions_by_type, name='get_institutions_by_type_api'),
    path('api/get_departments_by_institution_name/', views.get_departments_by_institution_name,name='get_departments_by_institution_name_api'),
    path('api/get_policies_by_department_name/', views.get_policies_by_department_name, name='get_policies_by_department_name_api'),

]


