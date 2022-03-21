from rest_framework.decorators import api_view
from rest_framework.response import Response
from online_store.models import Product, SubCategory
from django.shortcuts import get_object_or_404, redirect
from online_store.models import Order, OrderItem
from api import settings as api_settings
from django.core.mail import send_mail
from krd_samogon.settings import EMAIL_HOST_USER
from users.models import EmailsForMessages
from datetime import date
from krd_samogon.settings import MEDIA_URL, STATIC_URL


@api_view(['GET'])
def search_product(request):
    query = request.GET.get('query')
    products = list(
        Product.objects.filter(title__icontains=query).values('title', 'id')
    )

    return Response(products)


@api_view(['POST', 'DELETE'])
def purchases(request):
    if not request.user.is_authenticated:
        return api_settings.response_create_with_message(False, 'Вы не авторизовались')

    id_product = request.data.get('id_product')

    if request.method == 'POST':
        count = api_settings.check_int_value(request.GET.get('count'), 'count')
        if not count['result']: return count['error']
        else: count = count['value']
        if count < 0: return api_settings.RESPONSE_400
        product = get_object_or_404(Product, id=id_product)

        order, result_order = Order.objects.get_or_create(
            user=request.user,
            state=Order.StatusOrder.SHOPPINGLIST
        )

        order_item, result = OrderItem.objects.get_or_create(
            order=order, product=product
        )

        if not result:
            raise api_settings.RESPONSE_400_EXIST
        if result_order:
            order.date_state_shopping_list = date.today()
            order.save()

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
    if not request.user.is_authenticated:
        return api_settings.response_create_with_message(False, 'Вы не авторизовались')

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
    if not request.user.is_authenticated:
        return api_settings.response_create_with_message(False, 'Вы не авторизовались')

    if request.method == 'POST':
        value = api_settings.check_int_value(request.GET.get('value'), 'value')
        if not value['result']: return value['error']
        else: value = value['value']
        id_order_item = api_settings.check_int_value(request.GET.get('id_order_item'), 'id_order_item')
        if not id_order_item['result']: return id_order_item['error']
        else: id_order_item = id_order_item['value']

        if not OrderItem.objects.filter(id=id_order_item).exists():
            return api_settings.RESPONSE_400_NOT_EXISTS

        order_item = get_object_or_404(OrderItem, id=id_order_item)
        order_item.quantity = value
        order_item.save()

        price = order_item.get_cost()
        total_price = order_item.order.get_total_cost()
        result = {
            'success': 'true',
            'price': price,
            'total_price': total_price
        }

        return Response(result)

    return api_settings.RESPONSE_400


@api_view(['POST'])
def make_order(request):
    if not request.user.is_authenticated:
        return api_settings.response_create_with_message(False, 'Вы не авторизовались')

    if request.method == 'POST':
        emails = EmailsForMessages.objects.all()
        if emails.count() <= 0:
            return api_settings.response_create_with_message(
                True, 'Напишите на What`s app. Не указаны контакты администратора для отправки запроса'
            )
        order = get_object_or_404(Order, user=request.user, state=Order.StatusOrder.SHOPPINGLIST)
        items = order.items.all()
        if items.count() <= 0:
            redirect('online_store:index')

        subject = f'Заказ от пользователя {request.user.username}'
        from_email = EMAIL_HOST_USER
        message = f'Пользователь: {request.user.username}\nИмя: {request.user.first_name}\n'  \
            f'E-mail: {request.user.email}\nТелефон: {request.user.phone_number}\n\nЗаказ:\n'

        for item in items:
            message += f'{item.product.title} - {item.quantity}шт. Цена: {item.product.price}\n'

        message += f'\nИтого: {order.get_total_cost()}'

        send_mail(
            subject=subject, from_email=from_email, recipient_list=[email_recipient.email for email_recipient in emails],
            message=message
        )

        order.state = Order.StatusOrder.INPROCESSING
        order.date_state_in_processing = date.today()
        order.save()

        return api_settings.RESPONSE_SUCCESS

    return api_settings.RESPONSE_400


@api_view(['GET'])
def to_order_call(request):
    if not request.user.is_authenticated:
        return api_settings.response_create_with_message(False, 'Вы не авторизовались')

    seconds = api_settings.check_time_call_to_api(request.user, api_settings.SECONDS_FOR_ORDER_CALL)
    if seconds > 0:
        return api_settings.response_create_with_message(
            False,
            'Пока что вы не можете заказать звонок, ещё не прошло достаточно времени с предыдущего запроса.'
            f'\nОсталось {seconds}сек.'
    )

    if request.method == 'GET':
        emails = EmailsForMessages.objects.all()
        if emails.count() <= 0:
            return api_settings.response_create_with_message(
                True, 'Напишите на What`s app. Не указаны контакты администратора для отправки запроса'
            )

        user = request.user
        phone_number = user.phone_number
        name = user.first_name
        username = user.username
        email = user.email

        subject = f'Заказ звонка от {username}'
        from_email = EMAIL_HOST_USER
        message = f'Заказ звонка на номер: {phone_number}\n\nИмя: {name}\nE-mail: {email}'

        send_mail(
            subject=subject, from_email=from_email,
            recipient_list=[email_recipient.email for email_recipient in emails], message=message
        )

        return api_settings.response_create_with_message(True, f'Вы удачно заказали звонок на номер: {phone_number}')

    return api_settings.RESPONSE_400


@api_view(['GET'])
def get_subcategory_products(request):
    if request.method == 'GET':
        filter_date = True if request.GET.get('filter_date') == 'true' else False
        min_price = api_settings.check_int_value(request.GET.get('min_price'), 'min_price')
        if not min_price['result']: return min_price['error']
        else: min_price = min_price['value']
        max_price = api_settings.check_int_value(request.GET.get('max_price'), 'max_price')
        if not max_price['result']: return max_price['error']
        else: max_price = max_price['value']
        id_subcategory = api_settings.check_int_value(request.GET.get('id_subcategory'), 'id_subcategory')
        if not id_subcategory['result']: return id_subcategory['error']
        else: id_subcategory = id_subcategory['value']

        products = get_object_or_404(SubCategory, id=id_subcategory).in_products.filter(
            price__gte=min_price - 1, price__lte=max_price + 1
        ).order_by('-pub_date' if filter_date else 'pub_date').values('title', 'price', 'preview_image', 'id')

        return api_settings.response_create_with_message(
            True, {'products': products, 'media_url': MEDIA_URL, 'static_url': STATIC_URL}
        )

    return api_settings.RESPONSE_400
