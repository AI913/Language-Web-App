from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.db.models.aggregates import Count

import random
from random import sample, randint
from .models import Spanish, English

class LoginView(generic.DetailView):
	template_name = 'geniusdennis/login.html'

def email_check(user):
    return user.email.endswith('@example.com')

@user_passes_test(email_check)
def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/geniusdennis/')
    else:
    	return HttpResponseRedirect('')

class IndexView(generic.ListView):
    template_name = 'geniusdennis/index.html'
    context_object_name = 'latest_spanish_list'

    def get_queryset(self):
	    """
	    Return the last 20 spanish words (not including those set to be
	    published in the future).
	    """
	    latest_spanish_list = Spanish.objects.filter(
	        pub_date__lte=timezone.now()
	    ).order_by('-pub_date')[:20]
	    return latest_spanish_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
	    # grab the max id in the database
        #count = self.aggregate(count=Count('id'))['count']
        #random_index = randint(0, count - 1)
        #random_spanish = Spanish.objects.get(pk__gte= random_index)[:20]
        #return self.all()[random_index]
	    
        max_id = Spanish.objects.order_by('-id')[0].id
        random_id = random.randint(1, max_id + 1)
        random_spanish = Spanish.objects.filter(id__gte=random_id)[:20]
        context['random_spanish_list'] = random_spanish
        return context

class DetailView(generic.DetailView):
    model = Spanish
    template_name = 'geniusdennis/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Spanish.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Spanish
    template_name = 'geniusdennis/results.html'

class QuizView(generic.ListView):
	template_name = 'geniusdennis/quiz.html'
	queryset = Spanish.objects.all()

	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    # grab the max id in the database	    
	    max_id = Spanish.objects.order_by('-id')[0].id
	    random_id = random.randint(1, max_id + 1)
	    random_spanish_question = Spanish.objects.filter(id__gte=random_id)[0]
	    context['random_spanish_question'] = random_spanish_question
	    return context

def vote(request, spanish_id):
    spanish = get_object_or_404(Spanish, pk=spanish_id)
    try:
        selected_english = spanish.english_set.get(pk=request.POST['english'])
    except (KeyError, English.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'geniusdennis/detail.html', {
            'spanish': spanish,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_english.votes += 1
        selected_english.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('geniusdennis:results', args=(spanish.id,)))

def addword(request):
	newword_esp = Spanish(word_esp = request.POST['word_esp'], pub_date=timezone.now())
	newword_esp.save()
	newword_eng = English(word_eng = request.POST['word_eng'], spanish=newword_esp)
	newword_eng.save()
	return HttpResponseRedirect('/geniusdennis/')

def deleteword(request, spanish_id):
	word_to_delete = Spanish.objects.get(pk=spanish_id)
	word_to_delete.delete()
	return HttpResponseRedirect('/geniusdennis/')

def checkans(request, spanish_id):
	random_spanish_question = get_object_or_404(Spanish, pk=spanish_id)
	query = request.GET.get('ans')
	coreng = random_spanish_question.english_set.get()
	if query == str(coreng):
		#messages.success(request, "Correct!", extra_tags="correct")
		return render(request, ('geniusdennis/quiz.html'),{
				'message': "Correct!",
			})
		#return HttpResponseRedirect('geniusdennis/quiz.html')
	else:
		#messages.error(request, "Incorrect! The answer is " + str(coreng), extra_tags="incorrect")
		return render(request, 'geniusdennis/quiz.html', {
				'message': "Incorrect.",
				'correct_answer': "The correct answer is " + str(coreng),
			})
