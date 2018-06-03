from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.template import loader
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout


def create_user(request):
    template = loader.get_template('auth/create_user.html')
    context = {}
    return HttpResponse(template.render(context, request))


def create_user_form(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    new_user = User.objects.create_user(username, email, password)
    new_user.save()
    login(request, new_user)
    return HttpResponsePermanentRedirect('/users_quiz/')


def login_user(request):
    if request.user.is_authenticated:
        template = loader.get_template('user/users_quiz.html')
    else:
        template = loader.get_template('auth/login.html')
    context = {}
    return HttpResponse(template.render(context, request))


def login_form(request):
    username = request.POST['username']
    password = request.POST['password']
    new_user = authenticate(request, username=username, password=password)
    if new_user is not None:
        login(request, new_user)
        return HttpResponsePermanentRedirect('/quiz_list/')
    else:
        template = loader.get_template('auth/login.html')
        context = {'error': True}
        return HttpResponse(template.render(context, request))


def logout_user(request):
    logout(request)
    request.user = AnonymousUser()
    template = loader.get_template('auth/login.html')
    return HttpResponse(template.render({}, request))