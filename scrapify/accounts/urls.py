# accounts/urls.py
from django.urls import path
from . import views
# app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dual/', views.dual, name='dual'),
    path('logout/', views.log_out, name='log'),
    path('forgot_pass/', views.forgot_pass_view, name='forgot_pass'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('', views.home, name='home'),
]
