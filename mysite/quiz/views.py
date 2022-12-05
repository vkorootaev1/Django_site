import datetime

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views import View, generic
from django.views.generic import ListView

from .custom_decorators import anonymous_required, admin_required
from .forms import CustomUserCreationForm, MyAuthenticationForm, AnswerForm
from .models import *
from .utils import send_email_for_verify


# Create your views here.


class Number_of_not_answers(generic.base.ContextMixin):
    def get_context_data(self, *, object_list=None, **kwargs):
        try:
            now = datetime.datetime.now(tz=timezone.utc)
            count_active_quiz = Quiz.objects.filter(house=self.request.user.house.id, finished_at__gt=now)
            count_active_answers = Answer.objects.filter(quiz__in=count_active_quiz)
            count_active_not_answer = len(count_active_quiz) - len(count_active_answers)
            context = {
                'count': count_active_not_answer
            }
        except:
            context = {'count': 0}
        return super().get_context_data(**context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class All_quiz(Number_of_not_answers, ListView):
    paginate_by = 4
    model = Quiz
    template_name = 'quiz/quizes.html'
    context_object_name = 'list'

    def get_queryset(self):
        return Quiz.objects.filter(house=self.request.user.house.id).order_by('-created_at').prefetch_related(
            Prefetch('answer_set', queryset=Answer.objects.filter(user=self.request.user.id)))


@method_decorator(anonymous_required(login_url='home'), name='dispatch')
class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': CustomUserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        # print('Форма')
        # print(form)
        print('Запрос')
        print(request)
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


class News(Number_of_not_answers, ListView):
    paginate_by = 10
    queryset = News.objects.all().order_by('-created_at')
    template_name = 'quiz/news.html'
    context_object_name = 'news'


@method_decorator(anonymous_required(login_url='home'), name='dispatch')
class MyLoginView(LoginView):
    form_class = MyAuthenticationForm


def view_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id, house=request.user.house)
    try:
        now = datetime.datetime.now(tz=timezone.utc)
        count_active_quiz = Quiz.objects.filter(house=request.user.house.id, finished_at__gt=now)
        count_active_answers = Answer.objects.filter(quiz__in=count_active_quiz)
        count_active_not_answer = len(count_active_quiz) - len(count_active_answers)
        count = count_active_not_answer
    except:
        count = 0
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
    return render(request, 'quiz/quiz_answer.html', {"form": form, "quiz": quiz, "quiz_answer": quiz_answer, "count":count})


class MyPasswordChangeView(Number_of_not_answers, PasswordChangeView):
    pass


class MyPasswordChangeDoneView(Number_of_not_answers, PasswordChangeDoneView):
    pass


class MyPasswordResetView(Number_of_not_answers, PasswordResetView):
    pass


class MyPasswordResetDoneView(Number_of_not_answers, PasswordResetDoneView):
    pass


class MyPasswordResetConfirmView(Number_of_not_answers, PasswordResetConfirmView):
    pass


class MyPasswordResetCompleteView(Number_of_not_answers, PasswordResetCompleteView):
    pass


@method_decorator(admin_required(login_url='home'), name='dispatch')
class ManageHouses(ListView):
    model = House
    template_name = 'manage/view_houses.html'


@method_decorator(admin_required(login_url='home'), name='dispatch')
class ManageQuizes(ListView):
    context_object_name = 'list_quiz'
    template_name = 'manage/view_quizes.html'
    paginate_by = 5

    def get_queryset(self):
        return Quiz.objects.filter(house=self.kwargs['house_id']).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['house'] = House.objects.get(pk=self.kwargs['house_id'])
        return context


@method_decorator(admin_required(login_url='home'), name='dispatch')
class ManageAnswers(ListView):
    allow_empty = False
    model = Quiz
    template_name = 'manage/view_answers.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = get_object_or_404(Quiz, house=self.kwargs['house_id'], pk=self.kwargs['quiz_id'])
        context['house'] = House.objects.get(pk=self.kwargs['house_id'])
        context['count_answers_agree'] = Answer.objects.filter(quiz=self.kwargs['quiz_id'],
                                                               user__house=self.kwargs['house_id'], answer='T').count()
        context['count_answers_disagree'] = Answer.objects.filter(quiz=self.kwargs['quiz_id'],
                                                                  user__house=self.kwargs['house_id'],
                                                                  answer='F').count()
        return context
