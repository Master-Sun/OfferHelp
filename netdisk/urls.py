from django.urls import path
from netdisk import views


app_name = 'netdisk'
urlpatterns = [
    path('', views.index, name='index'),
]