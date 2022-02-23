from django.db import models

from .category import Category
from .characteristic import Characteristic


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, related_name='in_subcategories',
        on_delete=models.CASCADE,
        verbose_name='К какой категории относится',
        help_text='Укажите к какой категории относится подкатегория',
        blank=False, null=False
    )
    characteristics = models.ManyToManyField(
        Characteristic, related_name='in_subcategories',
        verbose_name='Характеристики',
        help_text='Укажите характеристики подкатегории',
        blank=False
    )
    title = models.CharField(
        max_length=40, unique=True, verbose_name='Заголовок',
        blank=False, null=False, help_text='Введите название подкатегории'
    )
    title_image = models.ImageField(
        verbose_name='Заголовочная картинка',
        help_text='Эта картинка показывается на странице подкатегории в '
        'заголовке',
        upload_to='subcategoryes_preview/',
        blank=False, null=False
    )
    image = models.ImageField(
        verbose_name='Картинка',
        help_text='Прикрепите картинку к подкатегории',
        upload_to='subcategoryes/',
        blank=False, null=False
    )

    class Meta:
        ordering = ('title',)
        verbose_name_plural = '   Подкатегории'

    def __str__(self):
        return f'Подкатегория: {self.title}'
