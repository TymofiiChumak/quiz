from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.template import loader
from .models import Quiz, Result, Question


def quiz_list(request):
    template = loader.get_template('user/list_quiz.html')
    list_of_quiz = Quiz.objects.all()
    context = {"list_of_quiz": list_of_quiz, "tmp_user": request.user}
    return HttpResponse(template.render(context, request))


def users_quiz(request):
    if request.user.is_anonymous:
        return HttpResponsePermanentRedirect('/quiz_list/')
    template = loader.get_template('user/users_quiz.html')
    list_of_quiz = Quiz.objects.filter(owner=request.user.id)

    class ResultItem:
        def __init__(self, title, correct, all_questions):
            self.title = title
            self.correct = correct
            self.all_questions = all_questions
    results = []

    for result in Result.objects.filter(user=request.user.id):
        all_questions = len(Question.objects.filter(quiz=result.quiz))
        results.append(ResultItem(result.quiz.title, result.correct_answers, all_questions))
    context = {"list_of_quiz": list_of_quiz, "results": results}
    return HttpResponse(template.render(context, request))