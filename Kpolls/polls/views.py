import random
from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Prompt, Choice, Idolranking, Submissions
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

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

        # stuff from deleted home app

        idols = Idolranking.objects.all()
        polls = Prompt.objects.all()

        for idol in idols:
            try:
                p = Choice.objects.get(choice_text__contains=idol.idol)
            except:
                pass
            else:
                idol.rank_votes = p.votes
                idol.save()
        context['artist_names'] = idols
        # end of stuff from deleted home app

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
        #only upvotes if poll has not ended
        past_prompts = [prompt for prompt in published_polls if prompt.rem_date <= timezone.now()] #re order to show newest first
        if prompt not in past_prompts: 
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', kwargs={'slug': slug}))
        else:
            return render(request, 'polls/detail.html', {
            'prompt': prompt,
            'error_message': "This poll has ended.",
            })
            return HttpResponseRedirect(reverse('polls:pollsindex'))

def submissions(request): 
    user_submission = Submissions(user_recommendation=request.POST['usubmissions'])
    if  user_submission.__str__() not in [num*' ' for num in range(1000)]:
        user_submission.save()
        messages.success(request, 'Thank you for your suggestion. Have a nice day!')
        return HttpResponseRedirect(reverse('polls:pollsindex'))
    else:
        messages.error(request, 'You didn\'t give a suggestion.')
        return HttpResponseRedirect(reverse('polls:pollsindex'))

    
    
