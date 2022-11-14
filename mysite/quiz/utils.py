from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator


def send_email_for_verify(request, user):
    context = {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
        'protocol': 'https'
    }
    message = render_to_string('registration/verify_email.html', context=context)
    email = EmailMessage('Подтвердите свой Email адрес', message, to=[user.email])
    email.send()
    if email.send:
        print('Отправлено!')
    else:
        print('Не отправлено!')

