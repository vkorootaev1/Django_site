from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .forms import CustomUserCreationForm, UserLoginForm
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout, get_user_model
from django.core.mail import EmailMessage, send_mail
from .models import *
from .tokens import account_activation_token
from django.conf import settings

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
            d = {'quiz': item.title}
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


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        print('Пользователь подвтердил свою почту')
        login(request, user)
        return redirect('home')
    else:
        print('Не получилось подтвердить почту')
    return redirect('home')

def activateEmail(request, user, to_email):
    # subject = "Activate your account"
    # print(to_email)
    # from_email = settings.DEFAULT_FROM_EMAIL
    # print(from_email)
    # message = 'This is my test message'
    # recipient_list = [to_email]
    # html_message =
    # email = send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)
    # if email:
    #     print('Отправлено')
    # else:
    #     print('Не отправлено')
    mail_subject = 'Activate your account'
    message = render_to_string(
        'quiz/verify_email.html', {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        }
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        print("Отправлено")
        return redirect('home')
    else:
        print("Не отправлено")


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
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