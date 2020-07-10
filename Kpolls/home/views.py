from django.shortcuts import render
from django.views import generic
from .models import Recommendation, Idolranking
from polls.models import Choice, Prompt


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'home/index.html'

    def get_queryset(self):
        return Idolranking.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #data to send to the index.html
        re = Recommendation.objects.all()[0]
        artists = Idolranking.objects.all()
        polls = Prompt.objects.all()

        for artist in artists:
            try:
                p = Choice.objects.get(choice_text__contains=artist.idol)
            except:
                pass
            else:
                artist.rank_votes = p.votes
                artist.save()

        choices = []
        choice_votes = []
        for choice in Choice.objects.all():
            if choice in artists:
                votes = choice.votes
                choices.append(choice)
                choices.append(votes)
        choice_votes_dict = dict(zip(choices, choice_votes))

        context['Choices'] = Choice.objects.all()
        context['choicevotes'] = choice_votes_dict
        context['artist_names'] = artists
        context['re'] = re
        context['polls'] = polls
        return context
