from django.db import models


class Category(models.Model):
    title = models.CharField(
        max_length=40, unique=True, verbose_name='Заголовок',
        blank=False, null=False, help_text='Введите название категории'
    )
    image = models.ImageField(
        verbose_name='Картинка категории',
        help_text='Прикрепите картинку к категории',
        upload_to='categoryes/',
        blank=False, null=False
    )
    title_image = models.ImageField(
        verbose_name='Заголовочная картинка',
        help_text='Эта картинка показывается на странице категории в '
        'заголовке',
        upload_to='categoryes_preview/',
        blank=False, null=False
    )

    class Meta:
        ordering = ('title',)
        verbose_name_plural = '    Категории'

    def __str__(self):
        return f'Категория: {self.title}'
