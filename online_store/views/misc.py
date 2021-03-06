from django.shortcuts import render


def page_not_found(request, exception):
    context = {
        'title': 'Ошибка 404',
        'title_h': '<span style="color: red">Ошибка. Код ошибки: 404</span>',
        'message': f'Страница <code>{request.path}</code> не найдена'
    }
    return render(request, 'customPage.html', context=context, status=404)


def server_error(request):
    context = {
        'title': 'Ошибка 500',
        'title_h': '<span style="color: red">Ошибка. Код ошибки: 500</span>',
        'message': 'Ошибка на сервере, попробуйте обновить '
        'страницу или обратиться позже'
    }
    return render(request, 'customPage.html', context=context, status=500)
