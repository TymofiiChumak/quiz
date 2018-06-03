from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Quiz(models.Model):
    title = models.CharField(max_length=40)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    correct = models.BooleanField()


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    correct_answers = models.IntegerField()

