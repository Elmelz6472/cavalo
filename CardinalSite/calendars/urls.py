from django.urls import path
from . import views

app_name = 'calendars'

urlpatterns = [
    path('', views.week_list, name='week_list'),
    path('create/', views.week_create, name='week_create'),
    path('<int:pk>/delete/', views.week_delete, name='week_delete'),
    path('<int:week_pk>/entries/', views.work_entry_list, name='work_entry_list'),
    path('<int:week_pk>/entries/create/', views.work_entry_create, name='work_entry_create'),
    path('<int:week_pk>/entries/<int:work_entry_pk>/delete/', views.work_entry_delete, name='work_entry_delete'),
]
