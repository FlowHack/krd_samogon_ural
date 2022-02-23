from rest_framework import status
from rest_framework.response import Response

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
