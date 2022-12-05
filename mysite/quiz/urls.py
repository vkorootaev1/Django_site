from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView

from .forms import *
from .views import *

urlpatterns = [
    path('quizes/', All_quiz.as_view(), name='quizes'),
    path('quiz/<int:quiz_id>/', view_quiz, name='view_quiz'),
    path('register/', Register.as_view(), name='register'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),
    path('invalid_verify', TemplateView.as_view(template_name='registration/invalid_verify.html'),
         name='invalid_verify'),
    path('confirm_email/', TemplateView.as_view(template_name='registration/confirm_email.html'), name='confirm_email'),
    path('login/', MyLoginView.as_view(next_page='home'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', News.as_view(), name='home'),
    path('reset_password/', MyPasswordResetView.as_view(template_name='registration/password_reset.html',
                                                        html_email_template_name='registration'
                                                                                 '/html_password_reset_email.html',
                                                        form_class=ResetPasswordForm), name='password_reset'),
    path('reset_password_sent/', MyPasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(template_name='registration'
                                                                                     '/password_reset_confirm.html',
                                                                       form_class=MySetPasswordForm),
         name='password_reset_confirm'),
    path('reset_password_complete/', MyPasswordResetCompleteView.as_view(template_name='registration'
                                                                                       '/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password_change/', MyPasswordChangeView.as_view(template_name='registration/password_change_form.html',
                                                          form_class=MyPasswordChangeForm), name='password_change'),
    path('password_change_done/', MyPasswordChangeDoneView.as_view(template_name='registration/password_change_done'
                                                                                 '.html'),
         name='password_change_done'),
    path('manage/', ManageHouses.as_view(), name='manage_houses'),
    path('manage/<int:house_id>/', ManageQuizes.as_view(), name='manage_quizes'),
    path('manage/<int:house_id>/<int:quiz_id>', ManageAnswers.as_view(), name='manage_answers')
]
