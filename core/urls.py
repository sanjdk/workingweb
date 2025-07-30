from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('register/confirm/', views.register_confirm, name='register_confirm'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
]
