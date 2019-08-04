from django.urls import path
from user import views

from django.contrib.auth import views as auth_view


app_name = 'user'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_view.LoginView.as_view(), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
]