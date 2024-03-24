from django.db import models
from django.contrib.auth.models import AbstractUser

from recommendation.users.managers import UserManager


# # Create your models here.
class User(AbstractUser):
    class USER_TYPE:
        """User type constants."""

        USER = "user"
        STAFF = "staff"

        CHOICES = (
            (USER, "User"),
            (STAFF, "Staff"),
        )

    name = None
    first_name = None
    last_name = None
    username = None
    email = models.EmailField(unique=True)
    type = models.CharField(
        max_length=10, default=USER_TYPE.USER, choices=USER_TYPE.CHOICES
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


# # Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField("self", blank=True, symmetrical=True)
    first_name = models.CharField(blank=True, max_length=255)
    last_name = models.CharField(blank=True, max_length=255)
