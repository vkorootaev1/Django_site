from django.urls import path
from django.views.generic import TemplateView

from .forms import MyPasswordChangeForm
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('register/', register, name='register'),
    path('quiz/<int:quiz_id>/', view_quiz, name='view_quiz'),
    path('register/', Register.as_view(), name='register'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),
    path('invalid_verify', TemplateView.as_view(template_name='registration/invalid_verify.html'), name='invalid_verify'),
    path('confirm_email/', TemplateView.as_view(template_name='registration/confirm_email.html'), name='confirm_email'),
    path('login/', MyLoginView.as_view(next_page='home'), name='login'),
    path('logout/', user_logout, name='logout'),
    path('', quizes, name='home'),
    # path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html', html_email_template_name='registration/html_password_reset_email.html'), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html', form_class=MyPasswordChangeForm), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done')
]
