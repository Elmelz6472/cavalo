from django.db import models


class Note(models.Model):
    content = models.TextField()
    last_modified = models.DateTimeField(auto_now=True)
