from django.db import models
# Create your models here.

class Recommendation(models.Model):
    song = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    upvote = models.IntegerField(default=0)

    def __str__(self):
        return self.song

class Idolranking(models.Model):
    rank_votes = models.CharField(max_length=200, default=0)
    idol = models.CharField(max_length=200)

    def __str__(self):
        return self.idol

