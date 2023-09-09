from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # Path: .../polls/
    path('', views.IndexView.as_view(), name='index'),
    # Path: .../polls/1/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # Path: .../polls/1/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # Path: .../polls/1/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
