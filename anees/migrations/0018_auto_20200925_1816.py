# Generated by Django 3.1.1 on 2020-09-25 18:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('anees', '0017_email_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='user',
        ),
        migrations.AddField(
            model_name='email',
            name='user',
            field=models.ManyToManyField(null=True, related_name='emailuser', to=settings.AUTH_USER_MODEL),
        ),
    ]
