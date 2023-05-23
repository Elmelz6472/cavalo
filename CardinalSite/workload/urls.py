from django.urls import path
from . import views

app_name = "workload"

urlpatterns = [
    path('', views.week_list, name='week_list'),
    path('create/', views.week_create, name='week_create'),
    path('detail/<int:pk>/', views.week_detail, name='week_detail'),
    path('delete/<int:pk>/', views.week_delete, name='week_delete'),
    path('edit/<int:week_pk>/<int:employee_pk>/<int:year>/<int:month>/<int:day>/', views.week_edit, name='week_edit'),
]
