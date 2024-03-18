from django.db import models

# from recommendation.users.models import Profile

class Movie(models.Model):
    class StreamingPlatforms:
        NETFLIX = 'netflix'
        AMAZON = 'amazon'

        CHOICES = (
            (NETFLIX, "Netflix StreamingPlatform"),
            (AMAZON, "Amazon StreamingPlatform")
        )

    title = models.CharField(max_length=255)
    release_date = models.DateField()
    streaming_platform = models.CharField(max_length=32, choices=StreamingPlatforms.CHOICES)
