from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Note
import json

@csrf_exempt
def note_view(request):
    note = Note.objects.first()
    if request.method == "POST":
        data = json.loads(request.body)
        note.content = data.get('content', '')
        note.last_modified = timezone.now()
        note.save()
        return JsonResponse({'last_modified': int(note.last_modified.timestamp())})
    return render(request, 'notes/note_view.html', {'note': note})
