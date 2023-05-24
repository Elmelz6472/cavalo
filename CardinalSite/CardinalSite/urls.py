from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('clients/', include('clients.urls', namespace="clients")),
    path('employees/', include("employees.urls", namespace="employees")),
    path('week/', include('week.urls', namespace='week')),
    path('notes/', include('notes.urls')),

]
