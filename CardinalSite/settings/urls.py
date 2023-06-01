from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('', views.settings, name='settings'),
    path('export/', views.export_data, name='export_data'),
    path('import/', views.import_data, name='import_data'),
    path('delete/', views.delete_database, name='delete_database'),
]