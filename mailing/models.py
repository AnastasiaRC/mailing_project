from django.db import models
from clients.models import Client
from message.models import Message
from users.models import User
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Mailing(models.Model):

    frequency_var = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    )

    status_var = (
        ('create', 'Создана'),
        ('started', 'Запущена'),
        ('ended', 'Завершена'),
    )

    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    contacts = models.ManyToManyField(Client, verbose_name='Контакты')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', **NULLABLE)
    time_start = models.DateTimeField(verbose_name='Время начала рассылки')
    time_end = models.DateTimeField(verbose_name='Время окончания рассылки')
    period = models.CharField(max_length=30, choices=frequency_var, default='daily', verbose_name='Периодичность')
    status = models.CharField(max_length=30, choices=status_var, default='create', verbose_name='Статус рассылки')

    def __str__(self):
        return f'{self.time_start}-{self.time_end}, {self.period}, {self.status}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Log(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    contacts = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Контакты')
    last_try_date = models.DateTimeField(default=timezone.now, verbose_name='Дата и время последней попытки')
    try_status = models.CharField(max_length=50, verbose_name='Статус попытки')
    server_answer = models.CharField(max_length=250, verbose_name='Ответ сервера', **NULLABLE)

    def __str__(self):
        return f'{self.last_try_date}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
