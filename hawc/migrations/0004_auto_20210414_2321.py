# Generated by Django 3.1.7 on 2021-04-14 23:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hawc', '0003_auto_20210410_0721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='author',
            name='is_staff',
        ),
        migrations.AddField(
            model_name='publication',
            name='sign_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='publication',
            name='status',
            field=models.CharField(choices=[('A', 'Signed'), ('R', 'Reject')], max_length=1),
        ),
    ]
