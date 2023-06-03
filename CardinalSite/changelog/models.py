from django.db import models
from django.utils import timezone

class ChangelogEntry(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.timestamp}: {self.message}'
