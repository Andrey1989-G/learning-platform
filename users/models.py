# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'null': True, 'blank': True}

class User(AbstractUser):

    username = models.EmailField(unique=True, null=True, verbose_name='username')
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='media/', verbose_name='аватар', **NULLABLE)
    auth_guid_code = models.CharField(max_length=36, verbose_name='код', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
