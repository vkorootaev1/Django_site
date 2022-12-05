from django.conf import settings
from django.contrib.auth.decorators import user_passes_test


# Custom user decorators


def anonymous_required(
        function=None, redirect_field_name=settings.ANONYMOUS_URL, login_url=None
):
    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def admin_required(
        function=None, redirect_field_name=settings.ADMIN_URL, login_url=None
):
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
