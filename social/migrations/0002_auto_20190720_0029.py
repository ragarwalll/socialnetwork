# Generated by Django 2.2.3 on 2019-07-19 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='users',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='users',
            name='location',
        ),
        migrations.AddField(
            model_name='users',
            name='userdata',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
