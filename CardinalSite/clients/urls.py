from django.urls import path
from . import views

app_name = "clients"

urlpatterns = [
    path('', views.client_list, name='client_list'),
    path('add/', views.client_create, name='client_create'),
    path('view/<int:pk>/', views.client_view, name='client_view'),
    path('edit/<int:pk>/', views.client_edit, name='client_edit'),
    path('delete/<int:pk>/', views.client_delete, name='client_delete'),
]
