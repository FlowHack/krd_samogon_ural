from django.db import models


class Characteristic(models.Model):
    title = models.CharField(
        verbose_name='Характеристика',
        help_text='Характеристика товара, название',
        max_length=100, null=False, blank=False
    )
    dimension = models.CharField(
        verbose_name='Измерение',
        help_text='Вы можете указать измерение характеристики.',
        max_length=40,
        null=True, blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['dimension', 'title'], name='unique dimension'
            )
        ]
        verbose_name_plural = '  Характерристики товара'

    def __str__(self):
        return f'{self.title} - {self.dimension}'
