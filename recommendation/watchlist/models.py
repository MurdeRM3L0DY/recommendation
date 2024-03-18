from django.contrib.auth import get_user_model
from django.db import models

from recommendation.movies.models import Movie

# Create your models here.
class WatchList(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
