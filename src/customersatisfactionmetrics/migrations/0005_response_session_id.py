# Generated by Django 4.2.7 on 2023-12-12 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customersatisfactionmetrics', '0004_question_is_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='session_id',
            field=models.CharField(default='default_session_id', max_length=128),
        ),
    ]
