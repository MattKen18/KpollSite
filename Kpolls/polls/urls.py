from django.urls import path


from . import views
from .models import Prompt, Choice

app_name = 'polls'
urlpatterns = [
    #the polls homepage where all the polls are
    path('', views.IndexView.as_view(), name='pollsindex'),

    #the unique page for each poll
    path('polls/<slug:slug>/', views.DetailView.as_view(), name='prompt_detail'),

    #the results page after vote
    path('polls/<slug:slug>/results/', views.ResultsView.as_view(), name='results'),

    #the vote url for voting for each prompt
    path('polls/<slug:slug>/vote/', views.vote, name='vote'),

    #the path that collects the user poll recommendations submissions on the homepage
    path('submission/', views.submissions, name='pollrecommend')
]
