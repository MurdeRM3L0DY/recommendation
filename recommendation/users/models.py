from django.db import models
from django.contrib.auth.models import AbstractUser

from recommendation.users.managers import UserManager


# # Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    friends = models.ManyToManyField("self", blank=True, symmetrical=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
