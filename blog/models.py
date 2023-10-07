from django.db import models
from mailing.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='media/blog/', verbose_name='Изображение', **NULLABLE)
    views_count = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    date = models.DateField(verbose_name='Дата публикации')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
