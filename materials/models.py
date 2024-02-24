from django.db import models

from django.conf import settings
from users.models import NULLABLE

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название курса')
    description = models.TextField(**NULLABLE, verbose_name='описание курса')
    preview = models.ImageField(upload_to='lesson/', **NULLABLE, verbose_name='изображение')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название урока')
    description = models.TextField(**NULLABLE, verbose_name='описание урока')
    preview = models.ImageField(upload_to='lesson/', **NULLABLE, verbose_name='изображение')
    video = models.CharField(max_length=250, **NULLABLE, verbose_name='ссылка на видео')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='название курса')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ['pk']

class SubscriptionsUserOnCourse(models.Model):
    course = models.ForeignKey(Course, models.CASCADE, verbose_name='курс', related_name='subscriptions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name='пользователь', related_name='subscriptions')

    is_active = models.BooleanField(default=False, verbose_name='активна')

    def __str__(self):
        return f'{self.user} - {self.course} - {self.is_active}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
