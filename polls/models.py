import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User


class Question(models.Model):
    """
    Class for question
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('date ended', null=True)

    def __str__(self):
        """
        String method
        """
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        """
        Return True if self.pub_date represents a point in time within
        the last 24 hours from the current time.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """
        Returns True if the current date is on or after question`s
        publication date.
        """
        return timezone.localtime() >= self.pub_date

    def can_vote(self):
        """
        Returns True if voting is allowed for this question.
        """
        if self.end_date:
            return timezone.localtime() < self.end_date
        return True


class Choice(models.Model):
    """
    Class for choice
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)

    @property
    def votes(self):
        """Return the number of votes for this choice."""
        # count = Vote.objects.filter(choice=self).count()
        return Vote.objects.filter(choice=self).count()

    def __str__(self):
        """
        String method
        """
        return self.choice_text


class Vote(models.Model):
    """Record a choice for a question made by a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Vote for {self.choice.choice_text}"
