from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class PasswordResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)



