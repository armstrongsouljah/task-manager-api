# Generated by Django 4.2.2 on 2023-06-24 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]