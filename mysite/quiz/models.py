from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    house = models.ForeignKey('House', on_delete=models.CASCADE)
    flat = models.IntegerField()
    email = models.EmailField(unique=True)
    email_verify = models.BooleanField(default=False)

    class Meta:
        unique_together = ['house', 'flat']


class House(models.Model):
    street = models.CharField(max_length=150)
    house = models.CharField(max_length=150)
    house_index = models.IntegerField()
    max_flat = models.IntegerField()

    def __str__(self):
        return f"{self.street} {self.house}"

    def get_absolute_url(self):
        return reverse('manage_quizes', kwargs={'house_id': self.pk})

    class Meta:
        unique_together = ['street', 'house']


class Quiz(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    house = models.ManyToManyField(House)
    finished_at = models.DateTimeField()

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('view_quiz', kwargs={'quiz_id': self.pk})

    def get_absolute_url_manage(self):
        return reverse('manage_answers', kwargs={'house_id': self.house, 'quiz_id': self.pk})

    class Meta:
        pass


answer_choice = [
        ('T', 'Согласен'),
        ('F', 'Не согласен')
    ]


class Answer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.CharField(choices=answer_choice, max_length=10)
    created_at = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True)

    def get_display_answer(self):
        return self.get_answer_display()

    def get_absolute_url(self):
        return reverse('view_quiz', kwargs={'quiz_id': self.pk})

    def __str__(self):
        return f"{self.quiz} {self.user} {self.get_answer_display()}"

    class Meta:
        unique_together = ['quiz', 'user']


class News(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True)


