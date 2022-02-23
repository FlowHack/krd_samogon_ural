from rest_framework.decorators import api_view
from rest_framework.response import Response
from online_store.models import Product
from django.shortcuts import get_object_or_404
from online_store.models import Order, OrderItem
from api import settings as api_settings
from django.core.mail import send_mail, send_mass_mail
from krd_samogon.settings import EMAIL_HOST_USER, EMAIL_HOST_ADMIN
from users.models import EmailsForMessages


@api_view(['GET'])
def search_product(request):
    query = request.GET.get('query')
    products = list(
        Product.objects.filter(title__icontains=query).values('title', 'id')
    )

    return Response(products)


@api_view(['POST', 'DELETE'])
def purchases(request):
    id_product = request.data.get('id_product')

    if request.method == 'POST':
        try:
            count = int(request.data.get('count'))
            if int(count) < 0:
                return api_settings.RESPONSE_400
        except ValueError:
            return api_settings.RESPONSE_400
        product = get_object_or_404(Product, id=id_product)

        order, result = Order.objects.get_or_create(
            user=request.user,
            state=Order.StatusOrder.SHOPPINGLIST
        )
        order_item, result = OrderItem.objects.get_or_create(
            order=order, product=product
        )

        if not result:
            raise api_settings.RESPONSE_400_EXIST

        order_item.quantity = int(count)
        order_item.save()

        return api_settings.RESPONSE_SUCCESS

    if request.method == 'DELETE':
        if Order.objects.filter(user=request.user, state=Order.StatusOrder.SHOPPINGLIST).exists():
            order = get_object_or_404(Order, user=request.user, state=Order.StatusOrder.SHOPPINGLIST)

            result = OrderItem.objects.filter(
                order=order, product__id=id_product
            ).delete()[0]

            if not result:
                return api_settings.RESPONSE_400_NOT_EXISTS
            return api_settings.RESPONSE_SUCCESS

    return api_settings.RESPONSE_400


@api_view(['DELETE'])
def shoppinglist(request):
    id_order_item = request.data.get('id_order_item')

    if request.method == 'DELETE':

        result = OrderItem.objects.filter(
            id=id_order_item
        ).delete()[0]
        if not result:
            return api_settings.RESPONSE_400_NOT_EXISTS

        return api_settings.RESPONSE_SUCCESS

    return api_settings.RESPONSE_400


@api_view(['POST'])
def change_count_product(request):
    if request.method == 'POST':
        value = int(request.data.get('value'))
        id_order_item = int(request.data.get('id_order_item'))

        if not OrderItem.objects.filter(id=id_order_item).exists():
            return api_settings.RESPONSE_400_NOT_EXISTS

        order_item = get_object_or_404(OrderItem, id=id_order_item)
        order_item.quantity = value
        order_item.save()

        price = order_item.get_cost()
        total_price = order_item.order.get_total_cost()
        result = {
            'result': 'true',
            'price': price,
            'total_price': total_price
        }

        return Response(result)

    return api_settings.RESPONSE_400


@api_view(['POST'])
def make_order(request):
    if request.method == 'POST':
        order = get_object_or_404(Order, user=request.user, state=Order.StatusOrder.SHOPPINGLIST)
        items = order.items.all()
        emails = EmailsForMessages.objects.all()

        subject = f'Заказ от пользователя {request.user.username}'
        from_email = EMAIL_HOST_USER
        message = f'Пользователь: {request.user.username}\nИмя: {request.user.first_name}\n'
        f'E-mail: {request.user.email}\nТелефон: {request.user.phone_number}\n\nЗаказ:\n'

        for item in items:
            message += f'{item.product.title} - {item.quantity}шт. Цена: {item.product.price}\n'

        message += '\nИтого: {order.get_total_cost()}'

        if emails.count == 1:
            send_mail(
                subject=subject, from_email=from_email, recipient_list=[emails[0].email],
                message=message
            )
        else:
            send_mass_mail(
                subject=subject, from_email=from_email, recipient_list=[email.email for email in emails],
                message=message
            )

        return Response({'result': 'true'})

    return api_settings.RESPONSE_400
