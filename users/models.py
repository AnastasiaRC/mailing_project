from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    іmage = models.ImageField(upload_to='media/users/', verbose_name='Картинка', **NULLABLE)
    phone = models.CharField(max_length=30, verbose_name='Телефон', **NULLABLE)
    is_manager = models.BooleanField(default=False, verbose_name='Менеджер')
    email = models.EmailField(unique=True, verbose_name='Email')
    is_active = models.BooleanField(default=False, verbose_name='Авторизация')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
