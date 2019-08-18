from django.urls import path
from user import views

from django.contrib.auth import views as auth_views


app_name = 'user'
urlpatterns = [
    path('register/', views.register, name='register'),
    # 使用django提供的视图类进行登入，登出，注册，密码修改等功能，只需要写好模板就行了，视图层不用写
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('active_email/', views.active_email, name='active_email'),
    path('email/send_active_code/', views.send_active_code, name='send_active_code'),
    path('refresh_captcha/', views.refresh_captcha, name='refresh_captch'),
]