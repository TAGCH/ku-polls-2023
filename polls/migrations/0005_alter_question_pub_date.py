# Generated by Django 4.2.4 on 2023-09-15 03:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_alter_question_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 15, 3, 51, 11, 475855, tzinfo=datetime.timezone.utc), verbose_name='date published'),
        ),
    ]
