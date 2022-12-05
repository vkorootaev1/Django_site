from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    house = models.ForeignKey('House', on_delete=models.CASCADE, verbose_name='Дом')
    flat = models.IntegerField(verbose_name='Квартира')
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    email_verify = models.BooleanField(default=False)

    class Meta:
        unique_together = ['house', 'flat']
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['id', 'username']


class House(models.Model):
    street = models.CharField(max_length=150, verbose_name='Улица')
    house = models.CharField(max_length=150, verbose_name='Номер дома')
    house_index = models.IntegerField(verbose_name='Индекс дома')
    max_flat = models.IntegerField(verbose_name='Количество квартир в доме')

    def __str__(self):
        return f"{self.street} {self.house}"

    def get_absolute_url(self):
        return reverse('manage_quizes', kwargs={'house_id': self.pk})

    class Meta:
        unique_together = ['street', 'house']
        verbose_name = "Дом"
        verbose_name_plural = "Дома"
        ordering = ['street', 'house']


class Quiz(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    text = models.TextField(blank=True, verbose_name='Текст опроса')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    house = models.ManyToManyField(House, 'Дом')
    finished_at = models.DateTimeField(verbose_name='Дата окончания')

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('view_quiz', kwargs={'quiz_id': self.pk})

    def get_absolute_url_manage(self):
        return reverse('manage_answers', kwargs={'house_id': self.house, 'quiz_id': self.pk})

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"
        ordering = ['created_at', '-finished_at']


answer_choice = [
        ('T', 'Согласен'),
        ('F', 'Не согласен')
    ]


class Answer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Опрос')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    answer = models.CharField(choices=answer_choice, max_length=10, verbose_name='Ответ')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    def get_display_answer(self):
        return self.get_answer_display()

    def get_absolute_url(self):
        return reverse('view_quiz', kwargs={'quiz_id': self.pk})

    def __str__(self):
        return f"{self.quiz} {self.user} {self.get_answer_display()}"

    class Meta:
        unique_together = ['quiz', 'user']
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        ordering = ['id', 'created_at']


class News(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст новости')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания новости')

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['id', 'created_at']

