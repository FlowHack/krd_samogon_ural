from django.core.validators import MinValueValidator
from django.db import models

from .characteristic import Characteristic


class QuantityCharacteristics(models.Model):
    characteristic = models.ForeignKey(
        Characteristic, on_delete=models.CASCADE,
        related_name='in_quantity_characteristics',
        verbose_name='Характеристика',
        help_text='Укажите к какой характеристике количество',
    )
    quantity = models.CharField(
        verbose_name='Значение',
        help_text='Укажите значение',
        null=False, blank=False,
        max_length=50
    )

    class Meta:
        ordering = ('characteristic',)
        verbose_name_plural = ' Кол-во характеристики'

    def __str__(self):
        return f'{self.characteristic.title} - {self.quantity} '  \
            f'{self.characteristic.dimension}'
