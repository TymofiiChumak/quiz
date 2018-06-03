from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Quiz, Question, Answer, Result


def index(request):
    return HttpResponsePermanentRedirect('login/')


def check_auth(func):
    def func_wrapper(request):
        if request.user.is_anonymous:
            return HttpResponsePermanentRedirect('/login/')
        else:
            return func(request)
    return func_wrapper


@check_auth
def create_quiz(request):
    template = loader.get_template('quiz/create_quiz.html')
    context = {}
    return HttpResponse(template.render(context, request))


@check_auth
def create_question(request):
    template = loader.get_template('quiz/create_question.html')
    indexes = ['0', '1', '2', '3', '4', '5']
    context = {'indexes': indexes}
    return HttpResponse(template.render(context, request))


@check_auth
def create_quiz_form(request):
    title = request.POST['title']
    user_id = request.user.id
    owner = User.objects.get(id=user_id)
    new_quiz = Quiz(title=title, owner=owner)
    new_quiz.save()
    request.session['quiz_id'] = new_quiz.id
    return HttpResponsePermanentRedirect('/create_question/')


@check_auth
def create_question_form(request):
    quiz_id = request.session['quiz_id']
    quiz = Quiz.objects.get(id=quiz_id)
    question_text = request.POST['question']
    question = Question.objects.create(quiz=quiz, text=question_text)
    question.save()
    for i in range(0, 6):
        answer_text = request.POST['text{}'.format(i)]
        if 'true{}'.format(i)in request.POST:
            answer_true = True
        else:
            answer_true = False
        if answer_text != '':
            answer = Answer.objects.create(question=question, text=answer_text, correct=answer_true)
            answer.save()
    return HttpResponsePermanentRedirect('/create_question/')


@check_auth
def successfully_created(request):
    template = loader.get_template('quiz/successfully_created.html')
    quiz_id = request.session['quiz_id']
    context = {'quiz_id': quiz_id}
    return HttpResponse(template.render(context, request))


def begin_quiz(request, quiz_id):
    template = loader.get_template('quiz/begin_quiz.html')
    quiz = Quiz.objects.get(id=quiz_id)
    title = quiz.title
    request.session['question'] = -1
    request.session['quiz_id'] = quiz_id
    context = {'title': title, 'quiz_id': quiz_id}
    return HttpResponse(template.render(context, request))


def pass_question(request):
    last = request.session['question']
    quiz = Quiz.objects.get(id=request.session['quiz_id'])
    has_next = True
    questions = Question.objects.filter(quiz=quiz).filter(id__gt=last).order_by('id')
    result = None
    if last == -1:
        user_id = request.user.id
        if user_id is None:
            result = Result.objects.create(user=None, quiz=quiz, correct_answers=0)
        else:
            result = Result.objects.create(user=User.objects.get(id=user_id), quiz=quiz, correct_answers=0)
        result.save()
        request.session['result_id'] = result.id
    elif len(request.POST) > 0:
        result = Result.objects.get(id=request.session['result_id'])
        if request.POST['True'] == 'OK':
            result.correct_answers += 1
            result.save()
    if len(questions) == 0:
        context = {"correct": result.correct_answers,
                   "all": len(Question.objects.filter(quiz=quiz)),
                   "title": quiz.title}
        template = loader.get_template('quiz/result.html')
        return HttpResponse(template.render(context, request))
    question = questions[0]

    if len(questions) < 2:
        has_next = False
    request.session['question'] = question.id
    answers = Answer.objects.filter(question=question)
    true_answers = answers.filter(correct=True).only('id')
    context = {'question': question.text, 'answers': answers, 'true_answers': true_answers, 'has_next': has_next}
    template = loader.get_template('quiz/pass_quiz.html')
    return HttpResponse(template.render(context, request))

