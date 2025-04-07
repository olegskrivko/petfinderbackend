from django.db import models

class Feedback(models.Model):
    sender = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255, default="Atsauksme")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} - {self.subject}"
