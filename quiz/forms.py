from django import forms


class CreateUserForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()


class CreateQuiz(forms.Form):
    title = forms.CharField()
    owner = forms.IntegerField()


class CreateQuestion(forms.Form):
    quiz = forms.IntegerField()
    text = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
