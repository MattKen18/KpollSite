import datetime
from django.urls import reverse
from django.test import TestCase, Client
from django.utils import timezone
from .models import *

# Create your tests here.

class PromptModelTest(TestCase):
    
    def test_was_published_recently_with_old_prompt(self):
        """
        was_published_recently() returns False for prompts whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_prompt = Prompt(pub_date=time)
        self.assertIs(old_prompt.was_published_recently(), False)

    
    def test_was_published_recently_with_future_prompt(self):
        """
        was_published_recently() returns False for prompts whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_prompt = Prompt(pub_date=time)
        self.assertIs(future_prompt.was_published_recently(), False)


    def test_was_published_recently_with_recent_prompt(self):
        """
        was_published_recently() returns True for prompts whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_prompt = Prompt(pub_date=time)
        self.assertIs(recent_prompt.was_published_recently(), True)


def create_prompt(prompt_text, days, slug):
    """
    Create a prompt with the given `prompt_text` and published the
    given number of `days` offset to now (negative for prompts published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    removal_date = time + datetime.timedelta(days=1)
    return Prompt.objects.create(prompt_text=prompt_text, pub_date=time, slug=slug, rem_date=removal_date)


class PollsIndexViewTests(TestCase):
    def test_no_prompts(self):
        """
        If no prompts exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:pollsindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available.")
        self.assertQuerysetEqual(response.context['prompt_of_the_day'], [])

    def test_future_prompt(self):
        """
        Prompts with a pub_date in the future aren't displayed on
        the index page.
        """
        create_prompt(prompt_text="Future prompt.", days=30, slug='future-prompt')
        response = self.client.get(reverse('polls:pollsindex'))
        self.assertContains(response, "No polls available.")
        self.assertQuerysetEqual(response.context['prompt_of_the_day'], [])

    def test_current_prompt(self):
        #checks if the current prompt is displayed on the index page

        create_prompt(prompt_text="Current prompt", days=0, slug='current-prompt')
        response = self.client.get(reverse('polls:pollsindex'))
        self.assertContains(response, "Current prompt")
        self.assertQuerysetEqual(response.context['prompt_of_the_day'], ['<Prompt: Current prompt>'])

    def test_past_prompts(self):
        #checks if past prompts list contains prompts that have ended

        past_prompt = create_prompt(prompt_text="past prompt", days=-10, slug='past-prompt')
        response = self.client.get(reverse('polls:pollsindex'))
        self.assertQuerysetEqual(response.context['past_prompts'], ['<Prompt: past prompt>'])

    def test_past_prompts_displayed(self):
        #checks if past prompts are displayed on the index page

        past_prompt = create_prompt(prompt_text="past prompt", days=-10, slug='past-prompt')
        response = self.client.get(reverse('polls:pollsindex'))
        self.assertContains(response, "past prompt")
        self.assertQuerysetEqual(response.context['past_prompts'], ['<Prompt: past prompt>'])


class PromptDetailViewTests(TestCase):

    def test_future_prompt(self):
        """
        The detail view of a prompt with a pub_date in the future
        returns a 404 not found.
        """
        future_prompt = create_prompt(prompt_text='Future prompt.', days=5, slug='future-prompt')
        url = reverse('polls:prompt_detail', args=(future_prompt.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_prompt(self):
        """
        The detail view of a prompt with a pub_date in the past
        displays the prompt's text.
        """
        past_prompt = create_prompt(prompt_text='Past Prompt.', days=-5, slug='past-prompt')
        url = reverse('polls:prompt_detail', kwargs={'slug': past_prompt.slug})
        response = self.client.get(url)
        self.assertContains(response, past_prompt.prompt_text)


class PromptResultsViewTests(TestCase):
    
    def test_past_prompt_ended(self):
        #checks if the poll displays as ended on the results page if it has ended

        past_prompt = create_prompt(prompt_text='Past Prompt', days=-5, slug='past-prompt')
        url = reverse('polls:results', kwargs={'slug': past_prompt.slug})
        response = self.client.get(url)
        self.assertContains(response, 'ended')

    def test_current_prompt_ongoing(self):
        #checks if the poll displays as ongoing on the results page if it has ended

        current_prompt = create_prompt(prompt_text='Current Prompt', days=0, slug='current-prompt')
        url = reverse('polls:results', kwargs={'slug': current_prompt.slug})
        response = self.client.get(url)
        self.assertContains(response, 'ongoing')

    def test_all_choices_shown(self):
        #checks if all the choices of the prompt is shown on the results page

        for prompt in Prompt.objects.all():
            url = reverse('polls:results', kwargs={'slug': prompt.slug})
            response = self.client.get(url)
            for choice in prompt.choice_set.all():
                self.assertContains(response, choice.choice_text)

    def test_correct_prompt(self):
        #checks if the prompt text on the results page is the correct one

        prompt = create_prompt(prompt_text='Prompt', days=0, slug='prompt')
        url = reverse('polls:results', kwargs={'slug': prompt.slug})
        response = self.client.get(url)
        self.assertContains(response, prompt.prompt_text)

class ChoiceVoteViewTests(TestCase):
    
    def test_vote_works(self):
        #checks if upvoting works

        fakeprompt = create_prompt(prompt_text='Fake Prompt', days=0, slug='fakeprompt')
        fakechoice1 = fakeprompt.choice_set.create(choice_text='Yes')
        fakechoice2 = fakeprompt.choice_set.create(choice_text='No')

        selected_choice = fakeprompt.choice_set.get(pk=1)
        
        for num in range(1, 101):     
            selected_choice.votes += 1
            selected_choice.save()
            self.assertEqual(selected_choice.votes, num)

class SubmissionsViewTests(TestCase):

    def test_submission_enters_database(self):
        #checks if submissions entered by users make it to the database
        for i in range(10):
            recommendation = "I need more polls about BTS {}".format(i)
            user_submission = Submissions(user_recommendation=recommendation)
            user_submission.save()
            response = self.client.get(reverse('polls:pollsindex'))

            self.assertQuerysetEqual([Submissions.objects.get(id=i+1)], ['<Submissions: I need more polls about BTS {}>'.format(i)])
