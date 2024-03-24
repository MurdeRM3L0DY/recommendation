from django.db import models


# Create your models here.
class WatchList(models.Model):
    profile = models.ForeignKey(
        "users.Profile", on_delete=models.CASCADE, related_name="user_profile"
    )
    movie = models.ForeignKey("movies.Movie", on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)

    class Meta:
        unique_together = ("profile", "movie")
