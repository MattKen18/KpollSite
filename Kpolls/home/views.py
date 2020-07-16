from django.shortcuts import render
from django.views import generic
from .models import Recommendation, Idolranking
from django.http import HttpResponseRedirect
from django.urls import reverse
from polls.models import Choice, Prompt


#LIST of all the recommendations so that a negative index can be used
recommendations_list = [re for re in Recommendation.objects.all()]

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'home/index.html'

    def get_queryset(self):
        return Idolranking.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #data to send to the index.html
        re = recommendations_list[-1] #gets the most recent recommendation
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

        #choices = []
        #choice_votes = []
        #for choice in Choice.objects.all():
        #    if choice in artists:
        #        votes = choice.votes
        #        choices.append(choice)
        #       choices.append(votes)
        #choice_votes_dict = dict(zip(choices, choice_votes))

        #context['Choices'] = Choice.objects.all()
        #context['choicevotes'] = choice_votes_dict
        context['artist_names'] = artists
        context['re'] = re
        context['polls'] = polls
        context['rec'] = recommendations_list
        return context

def heart_vote(request):
    selected_choice = recommendations_list[-1] #Recommendation.objects.get(pk=1)
    selected_choice.upvote += 1
    selected_choice.save()

    return HttpResponseRedirect(reverse('home:homeindex'))
