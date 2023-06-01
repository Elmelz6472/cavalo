# from django.contrib import admin
# from django.urls import path, include
# from django.contrib.auth import views as auth_views

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path('clients/', include('clients.urls', namespace="clients")),
#     path('employees/', include("employees.urls", namespace="employees")),
#     path('week/', include('week.urls', namespace='week')),
#     path('notes/', include('notes.urls')),
#     path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),

# ]

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

app_name = 'CardinalSite'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients/', include('clients.urls', namespace='clients')),
    path('employees/', include('employees.urls', namespace='employees')),
    path('week/', include('week.urls', namespace='week')),
    path('notes/', include('notes.urls', namespace='notes')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='clients:client_list'), name='logout')
    ]
