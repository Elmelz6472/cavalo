from django.shortcuts import render, redirect
from django.conf import settings as django_settings
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import connection
from datetime import date
from django.apps import apps
import os

@login_required
def settings(request):
    return render(request, 'settings/settings.html')


@login_required
def export_data(request):
    # Export the database to a db.sqlite3 file and send it as a response to download
    database_path = django_settings.DATABASES['default']['NAME']
    if os.path.exists(database_path):
        with open(database_path, 'rb') as f:
            today = date.today()
            filename = f"backup_{today.strftime('%B_%d')}.sqlite3"
            response = HttpResponse(f.read(), content_type='application/x-sqlite3')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        # Handle the case when the database file does not exist
        # You can redirect the user to an error page or show an appropriate message
        return HttpResponse('Database file does not exist.')

@login_required
def import_data(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        if file.name.endswith('.sqlite3'):
            # Save the uploaded file as db.sqlite3 to replace the existing database
            database_path = django_settings.DATABASES['default']['NAME']
            with open(database_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            messages.success(request, 'Database imported successfully.')
        else:
            messages.error(request, 'Invalid file format. Please select a valid SQLite database file.')
    else:
        messages.error(request, 'No file selected.')
    return redirect('settings:settings')


@login_required
def delete_database(request):
    if request.method == 'POST':
        confirm = request.POST.get('confirm', '')
        if confirm == 'confirmed':
            # Delete all tables from the database except superusers
            for model in apps.get_models():
                if model is not User:  # Exclude the User model (superusers)
                    model.objects.all().delete()

            messages.success(request, 'The database has been cleared except superusers.')
            return redirect('settings:settings')
        else:
            messages.error(request, 'Confirmation was not provided. Database deletion was canceled.')
            return redirect('settings:settings')

    return render(request, 'settings/delete_database.html')
    if request.method == 'POST':
        confirm = request.POST.get('confirm', '')
        if confirm == 'confirmed':
            # Delete the SQLite database file
            database_path = django_settings.DATABASES['default']['NAME']
            if os.path.exists(database_path):
                os.remove(database_path)

            # Recreate an empty database file
            open(database_path, 'w').close()

            messages.success(request, 'The database has been deleted.')
            return redirect('settings:settings')
        else:
            messages.error(request, 'Confirmation was not provided. Database deletion was canceled.')
            return redirect('settings:settings')

    return render(request, 'settings/delete_database.html')
    if request.method == 'POST':
        confirm = request.POST.get('confirm', '')
        if confirm == 'confirmed':
            # Delete the SQLite database file
            database_path = settings.DATABASES['default']['NAME']
            if os.path.exists(database_path):
                os.remove(database_path)

            # Recreate an empty database file
            with open(database_path, 'w'):
                pass

            messages.success(request, 'The database has been deleted.')
            return redirect('settings:settings')
        else:
            messages.error(request, 'Confirmation was not provided. Database deletion was canceled.')
            return redirect('settings:settings')

    return render(request, 'settings/delete_database.html')