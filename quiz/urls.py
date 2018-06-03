from django.urls import path, include

from . import auth_views
from . import user_views
from . import quiz_views


urlpatterns = [
    path('', quiz_views.index, name='index'),

    path('login/', auth_views.login_user, name='login'),
    path('login_form/', auth_views.login_form),
    path('create_user/', auth_views.create_user),
    path('create_user_form/', auth_views.create_user_form),
    path('logout/', auth_views.logout_user),

    path('create_quiz/', quiz_views.create_quiz, name='create quiz'),
    path('create_quiz_form/', quiz_views.create_quiz_form),
    path('create_question/', quiz_views.create_question, name='create question'),
    path('create_question_form/', quiz_views.create_question_form),
    path('successfully_created/', quiz_views.successfully_created),
    path('quiz/<int:quiz_id>/', quiz_views.begin_quiz),
    path('question/', quiz_views.pass_question),

    path('quiz_list/', user_views.quiz_list),
    path('users_quiz/', user_views.users_quiz),
]