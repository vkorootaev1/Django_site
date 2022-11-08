from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User)
admin.site.register(House)
admin.site.register(Quiz)
admin.site.register(Answer)
