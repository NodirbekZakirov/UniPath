import os  # работа с настройками системы

from django.core.wsgi import get_wsgi_application  # создаёт приложение для сервера

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unipath.settings")  # указываем файл настроек
application = get_wsgi_application()  # объект, который запускает веб-сервер
