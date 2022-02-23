from django import template
from online_store.models import Category, Order, OrderItem
from datetime import date

register = template.Library()


@register.simple_tag
def get_categories():
    return Category.objects.values('title', 'id')


@register.simple_tag
def get_year():
    return date.today().year


@register.filter
def has_shoplist(user):
    order, result = Order.objects.get_or_create(user=user, state=Order.StatusOrder.SHOPPINGLIST)
    count = order.items.count()
    return True if count > 0 else False


@register.filter
def in_shoplist(product, user):
    order, result = Order.objects.get_or_create(state=Order.StatusOrder.SHOPPINGLIST, user=user)
    return OrderItem.objects.filter(product=product, order=order).exists()
