from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Note
from django.contrib.auth.decorators import login_required

import json


@csrf_exempt
@login_required
def note_view(request):
    try:
        note = Note.objects.get()
    except Note.DoesNotExist:
        note = Note.objects.create(content="")

    if request.method == "POST":
        data = json.loads(request.body)
        note.content = data.get("content", "")
        note.last_modified = timezone.now()
        note.save()
        return JsonResponse({"last_modified": int(note.last_modified.timestamp())})

    return render(request, "notes/note_view.html", {"note": note})
