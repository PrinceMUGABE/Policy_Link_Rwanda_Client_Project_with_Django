from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account/signup/', views.signup, name='signup'),
    # path('activate/<str:token>/', views.activate, name='activate'),
    path('activate/<str:token>/', views.activate_account, name='activate'),
    path('account/view_all_users/', views.view_all_users, name='view_all_users'),
    path('account/user_edit/<int:user_id>', views.edit_user, name='edit_user'),
    path('account/delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('account/admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('account/user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('account/login/', views.user_login, name='login'),
    # path('account/login/otp_verification/', views.login_otp_verification, name='login_otp_verification'),
    path('account/logout/', views.logout_view, name='logout'),
    path('account/get_user/<int:user_id>/', views.get_user_by_id, name='get_user_by_id'),
    path('account/get_user/<str:username>/', views.get_user_by_username, name='get_user_by_username'),
    
    # Reports routes on users
    path('account/total_users/', views.total_users, name='total_users'),
    path('account/users_distribution/', views.users_distribution, name='users_distribution'),
    path('account/all_users/', views.all_users, name='all_users'),
    path('account/user_growth_over_months/', views.user_growth_over_years, name='user_growth_over_years'),
    path('account/reset_password/', views.reset_password, name='reset_password'),

    
    path('account/download_users_pdf/', views.download_users_pdf, name='download_users_pdf'),
    path('account/download_users_excel/', views.download_users_excel, name='download_users_excel'),
    
    path('contact-us/', views.contact_us, name='contact_us'),
]
