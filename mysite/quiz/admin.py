from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'house', 'flat')
    list_display_links = ('username', )
    search_fields = ('username', 'email')


class HouseAdmin(admin.ModelAdmin):
    list_display = ('street', 'house', 'house_index', 'max_flat')
    list_display_links = ('street', 'house')
    search_fields = ('street', 'house', 'house_index')


class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'finished_at')
    list_display_links = ('title', )
    search_fields = ('title', )


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'answer', 'user', 'created_at')
    list_display_links = ('quiz', 'user')
    search_fields = ('quiz', 'user')


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_display_links = ('title', )
    search_fields = ('title', )


admin.site.register(User, UserAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(News, NewsAdmin)
