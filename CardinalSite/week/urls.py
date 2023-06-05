from django.urls import path
from . import views

app_name = "week"

urlpatterns = [
    path("", views.week_list, name="week_list"),
    path("<int:pk>/", views.week_view, name="week_view"),
    path("new/", views.week_create, name="week_create"),
    path("<int:pk>/edit/", views.week_edit, name="week_edit"),
    path("<int:pk>/delete/", views.week_delete, name="week_delete"),
    path(
        "<int:week_pk>/employee/<int:employee_pk>/edit/",
        views.week_work_edit,
        name="week_work_edit",
    ),
    path("<int:pk>/export/", views.week_export, name="week_export"),
]
