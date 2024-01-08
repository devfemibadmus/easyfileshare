from django.db import models
from django.contrib.auth.models import User
import uuid

class FileManager(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    user_cache_key = models.CharField(max_length=255, blank=True, null=True)
    file_upload = models.FileField(upload_to='')
    auto_delete = models.BooleanField(default=False)
    shareable_link = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.file_upload.name
