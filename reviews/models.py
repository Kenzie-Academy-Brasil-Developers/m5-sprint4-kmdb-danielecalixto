from django.db import models



class Review(models.Model):
    
    class RecommendationType(models.TextChoices):
        MUST = "Must Watch"
        SHOULD = "Should Watch"
        AVOID = "Avoid Watch"
        NO = "No Opinion"

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
