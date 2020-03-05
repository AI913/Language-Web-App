import datetime
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Spanish

def create_spanish(word_esp, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Spanish.objects.create(word_esp=word_esp, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('geniusdennis:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Spanish words are available.")
        self.assertQuerysetEqual(response.context['latest_spanish_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_spanish(word_esp="Past question.", days=-30)
        response = self.client.get(reverse('geniusdennis:index'))
        self.assertQuerysetEqual(
            response.context['latest_spanish_list'],
            ['<Spanish: Past Spanish.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_spanish(word_esp="Future Spanish.", days=30)
        response = self.client.get(reverse('geniusdennis:index'))
        self.assertContains(response, "No Spanish words are available.")
        self.assertQuerysetEqual(response.context['latest_spanish_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_spanish(word_esp="Past Spanish word.", days=-30)
        create_spanish(word_esp="Future Spanish word.", days=30)
        response = self.client.get(reverse('geniusdennis:index'))
        self.assertQuerysetEqual(
            response.context['latest_spanish_list'],
            ['<Spanish: Past Spanish.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_spanish(word_esp="Past Spanish 1.", days=-30)
        create_spanish(word_esp="Past Spanish 2.", days=-5)
        response = self.client.get(reverse('geniusdennis:index'))
        self.assertQuerysetEqual(
            response.context['latest_spanish_list'],
            ['<Spanish: Past Spanish 2.>', '<Spanish: Past spanish 1.>']
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class SpanishModelTests(TestCase):

    def test_was_published_recently_with_future_spanish(self):
        """
        freshvocab() returns False for Spanish words whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_spanish = Spanish(pub_date=time)
        self.assertIs(future_spanish.freshvocab(), False)

    def test_was_published_recently_with_old_spanish(self):
	    """
	    was_published_recently() returns False for questions whose pub_date
	    is older than 1 day.
	    """
	    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
	    old_spanish = Spanish(pub_date=time)
	    self.assertIs(old_spanish.freshvocab(), False)

	def test_was_published_recently_with_recent_spanish(self):
	    """
	    was_published_recently() returns True for questions whose pub_date
	    is within the last day.
	    """
	    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
	    recent_spanish = Spanish(pub_date=time)
	    self.assertIs(recent_spanish.freshvocab(), True)