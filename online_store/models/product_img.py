from django.db import models
from .product import Product
from django.shortcuts import get_object_or_404


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        verbose_name='Товар', related_name='images',
        help_text='Укажите товар к которому прикрепить картинку',
        blank=False, null=False
    )
    image = models.ImageField(
        verbose_name='Картинка продукта',
        help_text='Прикрепите картинку к товару',
        upload_to='product_image/',
        blank=False, null=False
    )
    first = models.BooleanField(
        verbose_name='Первая картинка',
        help_text='Сделать эту картинку первой',
        blank=False
    )

    class Meta:
        ordering = ('product', 'first')
        verbose_name_plural = '     Картинки товаров'

    def save(self, *args, **kwargs):
        if self.first is True and  \
                ProductImage.objects.filter(first=True).exists():
            active_obj = get_object_or_404(ProductImage, first=True)
            active_obj.first = False
            active_obj.save()

        super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.title
