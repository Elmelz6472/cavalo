from django.urls import path
from . import views

app_name = "changelog"

urlpatterns = [
    path("", views.ChangelogView.as_view(), name="changelog_view"),
]
