import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class FileManager(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    file_name = models.CharField(max_length=40, blank=True, null=True)
    shareable_link = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    upload_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.shareable_link)
