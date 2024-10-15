from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    # Add a dummy field to force a migration
    dummy_field = models.BooleanField(default=False)

    def __str__(self):
        return self.username
