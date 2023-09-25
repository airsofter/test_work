from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Product(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название продукта'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_users',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class ProductUser(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_users',
        verbose_name='Продукт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_products',
        verbose_name='Пользователь'
    )

    class Meta:
        ordering = ('product', 'user')
        verbose_name = 'Связь продукта и пользователя'
        verbose_name_plural = 'Связи продуктов и пользователей'

    def __str__(self):
        return (f'Пользователь {self.user} подписан на '
                f'продукт {self.product}')


class Lesson(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название урока'
    )
    video = models.URLField(verbose_name='Ссылка на видео урока')
    viewing_duration = models.PositiveIntegerField(verbose_name='Длина видео')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_lessons',
        verbose_name='Продукт'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.name


class LessonUser(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='lesson_users',
        verbose_name='Урок'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_lessons',
        verbose_name='Пользователь'
    )
    viewing_status = models.BooleanField(verbose_name='Статус просмотра')
    date_last_view = models.DateTimeField(
        verbose_name='Время последнего просмотра'
    )

    class Meta:
        ordering = ('lesson', 'user')
        verbose_name = 'Связь урока и пользователя'
        verbose_name_plural = 'Связи уроков и пользователей'

    def __str__(self):
        return (f'Пользователь {self.user} является слушателем '
                f'урока {self.lesson}')
