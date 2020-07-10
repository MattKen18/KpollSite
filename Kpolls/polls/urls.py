from django.urls import path


from . import views
from .models import Prompt, Choice

app_name = 'polls'
urlpatterns = [
    #the polls homepage where all the polls are
    path('', views.IndexView.as_view(), name='pollsindex'),

    #the unique page for each poll
    path('<slug:slug>/', views.DetailView.as_view(), name='prompt_detail'),

    #the results page after vote
    path('<slug:slug>/results/', views.ResultsView.as_view(), name='results'),


    path('<slug:slug>/vote/', views.vote, name='vote'),
]
