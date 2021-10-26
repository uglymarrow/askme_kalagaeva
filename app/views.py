# from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here. контроллеры django.

def index(request):
    return render(request, "index.html", {})


questions = [
    {
        "title": f"Title {i}",
        "id" : i,
        "text": f"This is text for {i} questions."
    } for i in range(25)
]

def hot(request):
    paginator = Paginator(questions, 20)
    page = request.GET.get('page')
    content = paginator.get_page(page)

    return render(request, "hot.html", {'questions' : content})

def tag(request):
    return render(request, "index.html", {}) #что-то с этим сделать \ здесь должно быть имя тэга

def question(request):
    return render(request, "question.html", {}) #здесь должен быть номер вопроса

def login(request):
    return render(request, "login.html", {})

def signup(request):
    return render(request, "signup.html", {})

def ask(request):
    return render(request, "ask.html", {})