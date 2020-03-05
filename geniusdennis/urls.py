from django.urls import path

from . import views

app_name = 'geniusdennis'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    path('<int:spanish_id>/vote/', views.vote, name='vote'),
    path('quiz/', views.QuizView.as_view(), name='quiz'),
    path('checkans/<int:spanish_id>/', views.QuizView.as_view(),name='quiz'),
]