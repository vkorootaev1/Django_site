# Generated by Django 4.1.3 on 2022-11-06 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_alter_answer_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=models.CharField(choices=[('Да', 'Согласен'), ('Нет', 'Не согласен')], max_length=10),
        ),
    ]
