from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.views import View

from .forms import CustomUserCreationForm, UserLoginForm, MyAuthenticationForm, AnswerForm
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout, authenticate
from .models import *
from django.contrib.auth.tokens import default_token_generator as token_generator
from .utils import send_email_for_verify


# Create your views here.

# @user_passes_test(lambda u: u.is_superuser)
# def index(request):
#     if request.user.is_authenticated:
#         list_quiz_answer = []
#         id_house = request.user.house.id
#         id_user = request.user.id
#         print(f"Номер пользователя: {id_user}")
#         print(f"Номер дома: {id_house}")
#         all_quiz = Quiz.objects.filter(house=id_house)
#         for item in all_quiz:
#             d = {'quiz': item.title, 'created_at': item.created_at, 'finished_at': item.finished_at}
#             try:
#                 answer = Answer.objects.get(quiz=item.id, user=id_user)
#                 d['answer'] = answer.get_answer_display()
#             except:
#                 d['answer'] = 'Вы еще не проголосовали'
#             list_quiz_answer.append(d)
#         print(list)
#         context = {
#             'title': 'Главная',
#             'quiz': all_quiz,
#             'list': list_quiz_answer,
#         }
#     else:
#         context = {
#             'title': 'Главная'
#         }
#     return render(request, template_name='quiz/index.html', context=context)


def quizes(request):
    list_quiz_answer = []
    id_house = request.user.house.id
    id_user = request.user.id
    all_quiz = Quiz.objects.filter(house=id_house)
    for item in all_quiz:
        d = {"quiz": item}
        try:
            d["answer"] = Answer.objects.get(quiz=item.id, user=id_user)
        except:
            d["answer"] = "Вы еще не проголосовали"
        list_quiz_answer.append(d)
    return render(request, 'quiz/quizes.html', {"list": list_quiz_answer})

# def activate(request, uidb64, token):
#     User = get_user_model()
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except:
#         user = None
#
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         print('Пользователь подвтердил свою почту')
#         login(request, user)
#         return redirect('home')
#     else:
#         print('Не получилось подтвердить почту')
#     return redirect('home')


# def activateEmail(request, user, to_email):
#     # subject = "Activate your account"
#     # print(to_email)
#     # from_email = settings.DEFAULT_FROM_EMAIL
#     # print(from_email)
#     # message = 'This is my test message'
#     # recipient_list = [to_email]
#     # html_message =
#     # email = send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)
#     # if email:
#     #     print('Отправлено')
#     # else:
#     #     print('Не отправлено')
#     mail_subject = 'Activate your account'
#     message = render_to_string(
#         'quiz/verify_email.html', {
#             'user': user.username,
#             'domain': get_current_site(request).domain,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': account_activation_token.make_token(user),
#             'protocol': 'https' if request.is_secure() else 'http'
#         }
#     )
#     email = EmailMessage(mail_subject, message, to=[to_email])
#     if email.send():
#         print("Отправлено")
#         return redirect('home')
#     else:
#         print("Не отправлено")


# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             activateEmail(request, user, form.cleaned_data.get('email'))
#             return redirect('home')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'quiz/register.html', {"form": form})


# def user_login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserLoginForm
#     return render(request, 'quiz/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': CustomUserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            send_email_for_verify(request, user)
            return redirect('confirm_email')
        else:
            return render(request, self.template_name, {'form': form})


class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('home')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user


class MyLoginView(LoginView):
    form_class = MyAuthenticationForm


def view_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    try:
        quiz_answer = Answer.objects.get(quiz=quiz_id)
    except:
        quiz_answer = "Вы еще не проголосовали"
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data.get('answer')
            Answer.objects.create(quiz=quiz, user=User.objects.get(pk=request.user.id), answer=answer)
            return redirect('view_quiz', quiz_id)
    else:
        form = AnswerForm()
    return render(request, 'quiz/quiz_answer.html', {"form": form, "quiz": quiz, "quiz_answer": quiz_answer})


