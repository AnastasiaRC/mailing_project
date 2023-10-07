# Generated by Django 4.2.5 on 2023-10-04 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0002_initial'),
        ('message', '0001_initial'),
        ('mailing', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='contacts',
            field=models.ManyToManyField(to='clients.client', verbose_name='Контакты'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='message.message', verbose_name='Сообщение'),
        ),
        migrations.AddField(
            model_name='log',
            name='contacts',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.client', verbose_name='Контакты'),
        ),
        migrations.AddField(
            model_name='log',
            name='mailing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing', verbose_name='Рассылка'),
        ),
    ]