from django.db import models

# Create your models here.
from django.db import models

from course.models import Course
from users.models import NULLABLE


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название урока')
    description = models.TextField(**NULLABLE, verbose_name='описание урока')
    preview = models.ImageField(upload_to='lesson/', **NULLABLE, verbose_name='изображение')
    video = models.FileField(upload_to='videos/', **NULLABLE, verbose_name='видео')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='название курса')



    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'