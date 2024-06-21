from django.utils import timezone
from django.db import models

# Create your models here.
class SiteAdmin(models.Model):
    bankrupt = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    def __str__(self) -> str:
        return f'Bankrupt'