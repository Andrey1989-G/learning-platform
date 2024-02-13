from django.db import models

from users.models import NULLABLE


# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название курса')
    description = models.TextField(**NULLABLE, verbose_name='описание курса')
    preview = models.ImageField(upload_to='lesson/', **NULLABLE, verbose_name='изображение')


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'