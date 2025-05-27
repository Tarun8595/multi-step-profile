from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/summary/', views.profile_summary, name='profile_summary'),
    path('profile/view/', views.profile_view, name='profile_view'),
    path('login/', views.simple_login, name='login'),
    path('register/', views.simple_register, name='register'),
    
    # API endpoints
    path('api/check-username/', views.check_username, name='check_username'),
    path('api/states/', views.get_states, name='get_states'),
    path('api/cities/', views.get_cities, name='get_cities'),
]
