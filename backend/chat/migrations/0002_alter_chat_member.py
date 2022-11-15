# Generated by Django 4.1 on 2022-11-14 17:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='member',
            field=models.ManyToManyField(blank=True, default=None, related_name='chat_member', to=settings.AUTH_USER_MODEL),
        ),
    ]
