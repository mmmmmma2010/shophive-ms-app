from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    loyalty_points = models.IntegerField(default=0)
    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
