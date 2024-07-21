from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    """Модель курса"""
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец',
                              **NULLABLE)
    name = models.CharField(max_length=100, verbose_name='название курса', help_text='введите название курса')
    description = models.TextField(verbose_name='описание курса', help_text='введите описание курса', **NULLABLE)
    image = models.ImageField(upload_to='materials/course', verbose_name='изображение',
                              help_text='выберите изображение', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name='стоимость курса', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    """Модель урока"""
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец',
                              **NULLABLE)
    name = models.CharField(max_length=100, verbose_name='название урока', help_text='введите название')
    description = models.TextField(verbose_name='описание урока', help_text='введите описание', **NULLABLE)
    image = models.ImageField(upload_to='materials/lesson', verbose_name='изображение',
                              help_text='выберите изображение', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lesson_set', verbose_name='курс',
                               help_text='выберите курс')
    url = models.URLField(verbose_name='ссылка', help_text='добавьте ссылку', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name='стоимость урока', **NULLABLE)

    def __str__(self):
        return f"{self.name}, курс {self.course}"

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Subscription(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь',
                             **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    is_subscribed = models.BooleanField(default=False, verbose_name='наличие подписки', **NULLABLE)

    def __str__(self):
        return f'подписка {self.user} на курс {self.course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

