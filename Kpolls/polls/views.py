import random
from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Prompt, Choice
from home.models import Idolranking
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

published_polls = Prompt.objects.filter(pub_date__lte=timezone.now())

#this view is the polls homepage that has all the polls
class IndexView(generic.ListView):
    template_name = 'polls/index.html'

    def get_queryset(self):
        return Prompt.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        published_polls = Prompt.objects.filter(pub_date__lte=timezone.now()).order_by('-rem_date')
        context = super().get_context_data(**kwargs)

        #prompts in which the removal date has already passed
        past_prompts = [prompt for prompt in published_polls if prompt.rem_date <= timezone.now()] #re order to show newest first
        
        daily_prompts = [prompt for prompt in published_polls if prompt not in past_prompts]

        artists = [name.idol for name in Idolranking.objects.all()]

        for prompt in past_prompts:
            prompt.ended = True
            prompt.save()

        context["past_prompts"] = past_prompts
        context['prompt_of_the_day'] = daily_prompts
        context['artists'] = ' '.join(artists)
        return context

        #for every prompt in past prompts if the urls matches polls/prompt then redirect




#this view has the actual poll
class DetailView(generic.DetailView):
    model = Prompt
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Prompt.objects.filter(pub_date__lte=timezone.now())



class ResultsView(generic.DetailView):
    model = Prompt
    template_name = 'polls/results.html'
    #context_object_name = 'namesandvotes'

    def get_queryset(self):
        return Prompt.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prompt_names = []
        prompt_votes = []
        for prompt in Prompt.objects.all():
            total_votes_for_each = 0
            prompt_names.append(prompt.prompt_text)
            for choice in prompt.choice_set.all():
                total_votes_for_each += choice.votes
            prompt_votes.append(total_votes_for_each)

        context['namesandvotes'] = dict(zip(prompt_names, prompt_votes))
        return context
    



        #return render(request, 'polls/results.html', {'prompt': prompt})# add the things to send to html here

def vote(request, slug):
    prompt = get_object_or_404(Prompt, slug=slug)
    try:
        selected_choice = prompt.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
        'prompt': prompt,
        'error_message': "You didn't make a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', kwargs={'slug': slug}))
