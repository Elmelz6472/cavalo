from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.contrib.auth import views as auth_views

app_name = "CardinalSite"


def redirect_to_clients(request):
    return redirect("clients:client_list")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", redirect_to_clients, name="root"),
    path("clients/", include("clients.urls", namespace="clients")),
    path("employees/", include("employees.urls", namespace="employees")),
    path("week/", include("week.urls", namespace="week")),
    path("notes/", include("notes.urls", namespace="notes")),
    path("finance/", include("finance.urls", namespace="finance")),
    path("settings/", include("settings.urls", namespace="settings")),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="clients:client_list"),
        name="logout",
    ),
    path("changelog/", include("changelog.urls", namespace="changelog")),
]
