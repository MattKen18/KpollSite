import datetime
from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.

#to save the changes made to these models run the command python manage.py makemigrations polls
#run python manage.py migrate to apply these changes to the database

#this model is the actual poll question/prompt
class Prompt(models.Model):
    prompt_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    rem_date = models.DateTimeField('date removed', null=True)
    slug = models.SlugField(null=False, unique=True)
    ended = models.BooleanField(default=False)

    def __str__(self):
        return self.prompt_text

    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1 )

    def to_be_removed(self): #not really used
        return self.rem_date <= timezone.now()

    def get_absolute_url(self):
        return reverse('prompt_detail', kwargs={'slug': self.slug})

    def has_ended(self): #not really used
        return self.ended == True

#this model is the choices such as the different idol groups to choose from basesd on the particular prompt
class Choice(models.Model):
        prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
        choice_text = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)

        def __str__(self):
            return self.choice_text


class Idolranking(models.Model):
    rank_votes = models.CharField(max_length=200, default=0)
    idol = models.CharField(max_length=200)

    def __str__(self):
        return self.idol

class Submissions(models.Model):
    user_recommendation = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = "Submissions"

    def __str__(self):
        return self.user_recommendation