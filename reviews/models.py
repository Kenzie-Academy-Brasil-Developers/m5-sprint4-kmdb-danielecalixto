from django.db import models

class RecommendationType(models.TextChoices):
    MUST = ("M", "Must Watch")
    SHOULD = ("S", "Should Watch")
    AVOID = ("A", "Avoid Watch")
    NO = ("NO", "No Opinion")

class Review(models.Model):
    stars = models.IntegerField()
    review = models.TextField()
    spoilers = models.BooleanField()
    recommendation = models.CharField(
        max_length=50,
        choices=RecommendationType.choices,
        default=RecommendationType.NO
    )

    movie = models.ForeignKey("movies.Movie", on_delete=models.CASCADE, related_name="reviews")
    critic = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reviews")
