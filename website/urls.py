from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_user_files/', views.get_user_files, name='get_user_files'),
    path('file_upload/', views.file_upload, name='file_upload'),
    path('file_delete/<str:shareable_link>/', views.file_delete, name='file_delete'),
    path('view_file/<str:shareable_link>/', views.view_file, name='view_file'),
]
