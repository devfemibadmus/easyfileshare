from django.urls import path, re_path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_user_files/', views.get_user_files, name='get_user_files'),
    path('file_upload/', views.file_upload, name='file_upload'),
    path('file_delete/<str:shareable_link>/', views.file_delete, name='file_delete'),
    path('download/<str:shareable_link>', views.download, name='download'),
    re_path(r'^.*$', RedirectView.as_view(pattern_name='home', permanent=False)),
]
