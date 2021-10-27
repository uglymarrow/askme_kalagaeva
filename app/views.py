# from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here. контроллеры django.

questions = [
    {
        "title": f"Title {i}. Where is Jiraiya? ",
        "id" : i,
        "text": f"This is text for {i} questions. What's your wish? Peace? Money? Or the world? Whatever you wish for, it's something you have to get with your own strength!"
    } for i in range(25)
]


def index(request):
    paginator = Paginator(questions, 20)
    page = request.GET.get('page')
    content = paginator.get_page(page)

    return render(request, "index.html", {'questions':content})

def hot(request):
    paginator = Paginator(questions, 20)
    page = request.GET.get('page')
    content = paginator.get_page(page)

    return render(request, "hot.html", {'questions':content})

def tag(request):
    return render(request, "index.html", {}) #что-то с этим сделать \ здесь должно быть имя тэга

comments = [
    {
        "text": f"This is comment number {i}."
    } for i in range(25)
]

def question(request, id):
    paginator = Paginator(comments, 20)
    page = request.GET.get('page')
    content = paginator.get_page(page)

    return render(request, "question.html", {'comments': content, 'question':questions[id]}) #здесь должен быть номер вопроса

def login(request):
    return render(request, "login.html", {})

def signup(request):
    return render(request, "signup.html", {})

def ask(request):
    return render(request, "ask.html", {})