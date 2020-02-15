from django.urls import path
from netdisk import views


app_name = 'netdisk'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('create_dir/', views.create_dir, name='create_dir'),
    path('entry_dir/<int:dir_id>/', views.entry_dir, name='entry_dir'),
    path('delete/', views.delete_file, name='delete_file')
]