# Generated by Django 2.2.4 on 2019-08-17 08:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_emailverifyrecord'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailverifyrecord',
            name='send_time',
        ),
        migrations.AddField(
            model_name='emailverifyrecord',
            name='expire_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='过期时间'),
            preserve_default=False,
        ),
    ]
