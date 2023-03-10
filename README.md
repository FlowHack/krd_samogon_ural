# КраснодарСамогонУрал

<h2 style="color: red">Проект закрыт и не поддерживаетя!</h2>

## ***Технологии***
```
Python 3.8.5
Django 4.0
phonenumbers 8.12.45
```

## ***Запуск при помощи python 3.8.5***
* Для начала создайте виртуальное окружение и установите зависимости
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

* Выполните миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

* Создайте суперпользователя
```bash
python manage.py createsuperuser
python manage.py makemigrations
python manage.py migrate
```
* Запустите сервер
```bash
python manage.py runserver
```

