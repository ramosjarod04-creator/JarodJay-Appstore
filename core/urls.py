from django.urls import path
from . import views

urlpatterns = [
    path('', views.app_list, name='app_list'),
    path('upload/', views.upload_app, name='upload_app'),
    path('delete/<int:pk>/', views.delete_app, name='delete_app'), # Add this line
]