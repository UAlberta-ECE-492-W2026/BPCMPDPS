from django.conf import settings
from django.db import models

class OperatorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=32, blank=True)
    alerts_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"OperatorProfile({self.user.username})"