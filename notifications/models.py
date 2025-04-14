# notifications/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PushSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey if one user can have multiple subscriptions
    endpoint = models.URLField()
    p256dh = models.CharField(max_length=255)
    auth = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s subscription"
