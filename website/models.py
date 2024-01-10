import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class FileManager(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    file_upload = models.FileField(upload_to='media/')
    shareable_link = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    upload_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.file_upload.name

    def delete(self, *args, **kwargs):
        self.file_upload.delete()
        super().delete(*args, **kwargs)
