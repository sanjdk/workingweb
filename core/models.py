
from django.db import models
from django.contrib.auth.models import User

# Application model to store all application details
class Application(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='application')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=300, blank=True)
    project_title = models.CharField(max_length=300)
    supervisor = models.CharField(max_length=200, blank=True)
    cycle = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='Incomplete')
    progress = models.PositiveIntegerField(default=0)
    submitted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.project_title}"
