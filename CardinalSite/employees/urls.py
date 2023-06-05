from django.urls import path
from . import views

app_name = "employees"

urlpatterns = [
    path("", views.employee_list, name="employee_list"),
    path("add/", views.employee_create, name="employee_create"),
    path("update/<int:pk>/", views.employee_update, name="employee_update"),
    path("delete/<int:pk>/", views.employee_delete, name="employee_delete"),
    path("<int:pk>/", views.employee_view, name="employee_view"),
    path("export/", views.employee_export, name="employee_export"),
]
