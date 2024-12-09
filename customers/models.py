# In your models.py file

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(AbstractUser):
    username = models.CharField(max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
