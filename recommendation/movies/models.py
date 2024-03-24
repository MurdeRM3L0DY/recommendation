from django.db import models

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

    class Meta:
        unique_together = ("title", "release_date")
