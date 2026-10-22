import os  # Получаем доступ к переменным окружения | import подключает модуль по имени.
from django.core.wsgi import get_wsgi_application  # Импортируем фабрику WSGI-приложения | from/import подключают указанные имена.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unipath.settings")  # Указываем настройки UniPath | setdefault — задаёт значение ключа только если ключ ещё отсутствует.
application = get_wsgi_application()  # Создаём объект, принимающий HTTP-запросы от сервера | get_wsgi_application — создаёт Django-приложение для совместимого WSGI-сервера.
