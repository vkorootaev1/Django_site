# Generated by Django 4.1.3 on 2022-11-05 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='flat',
            field=models.IntegerField(blank=True),
        ),
    ]
