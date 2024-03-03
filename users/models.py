# Create your models here.
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'null': True, 'blank': True}

class User(AbstractUser):
    # поправляю замечания наставника
    # пришлось вернуть определенное поле username так как сериализатор выдавал ошибку
    username = models.EmailField(unique=True, null=True, verbose_name='username')
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='media/', verbose_name='аватар', **NULLABLE)
    auth_guid_code = models.CharField(max_length=36, verbose_name='код', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле имэйл должен быть заполнен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
