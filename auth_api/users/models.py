from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

import uuid
from datetime import datetime, timedelta
from django.utils import timezone
class User(models.Model):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(minutes=5)


# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)
#     otp = models.CharField(max_length=6, blank=True, null=True)
#     otp_created_at = models.DateTimeField(blank=True, null=True)
#     last_otp_sent = models.DateTimeField(blank=True, null=True)
#     otp_resend_count = models.IntegerField(default=0)
#     pass


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email