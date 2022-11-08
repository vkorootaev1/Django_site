from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, UserLoginForm
from django.core.exceptions import ValidationError
from django.contrib.auth import login,logout

from .models import *


# Create your views here.


def index(request):
    if request.user.is_authenticated:
        list = []
        id_house = request.user.house.id
        id_user = request.user.id
        print(f"Номер пользователя: {id_user}")
        print(f"Номер дома: {id_house}")
        all_quiz = Quiz.objects.filter(house=id_house)
        for item in all_quiz:
            d = {}
            d['quiz'] = item.title
            try:
                answer = Answer.objects.get(quiz=item.id, user=id_user)
                d['answer'] = answer.get_answer_display()
            except:
                d['answer'] = 'Вы еще не проголосовали'
            list.append(d)
        print(list)
        context = {
            'title': 'Главная',
            'quiz': all_quiz,
            'list': list,
        }
    else:
        context = {
            'title': 'Главная'
        }
    return render(request, template_name='quiz/index.html', context=context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'quiz/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm
    return render(request, 'quiz/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')