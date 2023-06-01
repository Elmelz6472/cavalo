from django.db import models

class DatabaseBackup(models.Model):
    backup_file = models.FileField(upload_to='backups/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.backup_file.name
