from django.db import models
import uuid
from django.contrib.auth.models import User

class STUDENT(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)
    confirm_password = models.CharField(max_length=255, blank=False, null=False)

class STUDENTINFO(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    college = models.CharField(max_length=255, blank=False, null=False)
    phone = models.CharField(max_length=255, blank=False, null=False)
    bkash_number = models.CharField(max_length=255,blank=False, null=False)
    is_approved = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)