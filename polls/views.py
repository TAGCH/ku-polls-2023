from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        now = timezone.now()
        pub = '-pub_date'
        return Question.objects.filter(pub_date__lte=now).order_by(pub)[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """Check if the question can be voted."""
        user = request.user
        try:
            question = get_object_or_404(Question, pk=kwargs['pk'])
        except Http404:
            messages.error(request,
                           "This question is not available for voting.")
            return HttpResponseRedirect(reverse('polls:index'))

        try:
            if not user.is_authenticated:
                raise Vote.DoesNotExist
            user_vote = question.vote_set.get(user=user).choice
        except Vote.DoesNotExist:
            # if user didn't select a choice or invalid choice
            # it will render as didn't select a choice
            return super().get(request, *args, **kwargs)
            # go to polls detail
        return render(request, 'polls/detail.html', {
                'question': question,
                'user_vote': user_vote,
            })


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """Vote for one of the answers to a question."""
    user = request.user
    print("current user is", user.id, "login", user.username)
    print("Real name:", user.first_name, user.last_name)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if question.can_vote():
            try:
                # find a avote for this user and this question
                user_vote = question.vote_set.get(user=user)
                user_vote.choice = selected_choice
                user_vote.save()
            except Vote.DoesNotExist:
                # no matching vote - create a new vote
                Vote.objects.create(user=user,
                                    choice=selected_choice,
                                    question=selected_choice.question).save()
        else:
            messages.error(request, "You can't vote this question.")
            return HttpResponseRedirect(reverse('polls:index'))
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # get named fields from the form data
            username = form.cleaned_data.get('username')
            # password input field is named 'password1'
            raw_passwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_passwd)
            login(request, user)
            return redirect('polls:index')
        # what if form is not valid?
        # we should display a message in signup.html
    else:
        # create a user form and display it the signup page
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
