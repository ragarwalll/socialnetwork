# Generated by Django 2.2.3 on 2019-07-21 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0004_auto_20190721_0151'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='userdata',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='social.Users'),
            preserve_default=False,
        ),
    ]
