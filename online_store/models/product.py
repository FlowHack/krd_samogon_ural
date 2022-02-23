from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MinValueValidator
from django.db import models

from .subcategory import SubCategory
from .quantity_characteristic import QuantityCharacteristics


class Product(models.Model):
    subcategory = models.ForeignKey(
        SubCategory, related_name='in_products',
        on_delete=models.CASCADE,
        verbose_name='Категория',
        help_text='Укажите к какой категории относится товар',
        blank=False, null=False
    )
    characteristics = models.ManyToManyField(
        QuantityCharacteristics, related_name='in_products',
        verbose_name='Характеристики',
        help_text='Укажите характеристики продукта. Все характеристики '
        'подкатегории должны быть указаны у этого продукта!',
        blank=False
    )
    equipment = models.TextField(
        verbose_name='Комплектация',
        help_text='Через "&&" укажите комплект. Пример: "Предмет&&Ложка&&Вилка&&Тарелька"',
        blank=True
    )
    title = models.CharField(
        verbose_name='Название',
        help_text='Укажите название товара',
        max_length=40, null=False, blank=False, unique=True
    )
    price = models.FloatField(
        verbose_name='Цена',
        help_text='Укажите цену товара',
        null=False, blank=False,
        validators=[MinValueValidator(0.1)]
    )
    description = RichTextUploadingField(
        config_name='default', verbose_name='Описание',
        help_text='Вы можете указать описание продукта',
        blank=True, null=False
    )
    preview_image = models.ImageField(
        verbose_name='Превью картинка продукта',
        help_text='Прикрепите превью картинку к товару (показывается в карточке)',
        upload_to='product_preview_image/',
        blank=False, null=False, default='product.jpeg'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = '      Товары'

    def __str__(self):
        return f'Продукт {self.title}'
