from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone

RESPONSE_SUCCESS = Response({'success': 'true'})
RESPONSE_400_EXIST = Response(
    {'success': 'false', 'error': 'Такой объект уже имеется'},
    status=status.HTTP_400_BAD_REQUEST
)
RESPONSE_400_NOT_EXISTS = Response(
    {'success': 'false', 'error': 'Нет такого объекта'},
    status=status.HTTP_400_BAD_REQUEST
)
RESPONSE_400 = Response(
    {'success': 'false', 'error': 'Неверный запрос'},
    status=status.HTTP_400_BAD_REQUEST
)

SECONDS_FOR_ORDER_CALL = 20
SECONDS_FOR_GET_PRODUCTS_SUBCATEGORY = 2


def response_create_with_message(result, message):
    response = {'success': 'false' if not result else 'true'}
    response.update({'message': message} if result else {'error': message})

    return Response(response)


def check_time_call_to_api(user, sec):
    time_user = user.time_call_to_api
    time = timezone.now()

    difference = time - time_user
    difference = difference.total_seconds()

    if difference >= sec:
        user.time_call_to_api = time
        user.save()

    return 0 if difference >= sec else round(sec - difference)


def check_int_value(value, name):
    if value is not None:
        try:
            return {'result': True, 'value': int(value)}
        except ValueError:
            return {
                'result': False,
                'error': response_create_with_message(
                    False, f'Неверно указано {name} в запросе \nНапишите нам в What`s app с найденной ошибкой!'
                )
            }
    else:
        return {'result': False, 'error': response_create_with_message(False, f'Не указано значение {name}')}
