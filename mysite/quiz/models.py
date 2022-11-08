from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_max_flat


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

    class Meta:
        unique_together = ['street', 'house']


class Quiz(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    house = models.ManyToManyField(House)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        pass


class Answer(models.Model):
    answer_choice = [
        ('T', 'Согласен'),
        ('F', 'Не согласен')
    ]
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.CharField(choices=answer_choice, max_length=10)
    created_at = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.quiz} {self.user} {self.get_answer_display()}"

    class Meta:
        unique_together = ['quiz', 'user']




