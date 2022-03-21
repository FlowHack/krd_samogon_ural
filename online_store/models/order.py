from django.db import models
from django.contrib.auth import get_user_model
from .product import Product
from datetime import date

User = get_user_model()


class Order(models.Model):

    class StatusOrder(models.TextChoices):
        SHOPPINGLIST = 'Корзина', 'shopping_cart'
        INPROCESSING = 'В обработке', 'in_processing'
        INDELIVERY = 'Отправлен', 'in_delivery'
        ORDERCOMPLETE = 'Получен', 'order_complete'

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='in_orders',
        verbose_name='Пользователь',
        help_text='Выберите пользователя'
    )
    date_state_shopping_list = models.DateField(
        verbose_name='Дата установки статуса "Корзина"',
        help_text='По умолчанию - дата создания записи',
        default=date.today, null=False, blank=False
    )
    date_state_in_processing = models.DateField(
        verbose_name='Дата установки статуса "В обработке"',
        help_text='По умолчанию - дата создания записи. (Если не был переведён в статус "В обработке")',
        default=date.today, null=False, blank=False
    )
    date_state_in_delivery = models.DateField(
        verbose_name='Дата установки статуса "Отправлен"',
        help_text='По умолчанию - дата создания записи. (Если не был переведён в статус "Отправлен")',
        default=date.today, null=False, blank=False
    )
    date_state_complete = models.DateField(
        verbose_name='Дата установки статуса "Получен"',
        help_text='По умолчанию - дата создания записи. (Если не был переведён в статус "Получен")',
        default=date.today, null=False, blank=False
    )
    state = models.TextField(
        verbose_name='Статус заказа',
        choices=StatusOrder.choices,
        default=StatusOrder.SHOPPINGLIST
    )

    class Meta:
        verbose_name_plural = '       Заказы пользователей'

    def __str__(self):
        return f'{self.user.first_name} State: {self.state}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_count_items(self):
        return self.items.count()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ',
        help_text='К какому заказу относится'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='in_orders', verbose_name='Товар',
        help_text='Выберите рецепт'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество товара', help_text='Укажите количество заказываемого товара',
        default=1
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'product'], name='unique product'
            )
        ]
        verbose_name_plural = '      Составляющие заказов'

    def __str__(self):
        return self.order.user.first_name

    def get_cost(self):
        return self.product.price * self.quantity
