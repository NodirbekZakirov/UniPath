import os  # Импортируем доступ к переменным окружения операционной системы | import подключает модуль по имени.
import sys  # Получаем список аргументов командной строки | import подключает модуль по имени.
from django.core.management import execute_from_command_line  # Импортируем обработчик команд Django | from/import подключают указанные имена.
if __name__ == "__main__":  # Выполняем запуск только при непосредственном вызове файла.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unipath.settings")  # Указываем модуль настроек проекта | setdefault — задаёт значение ключа только если ключ ещё отсутствует.
    execute_from_command_line(sys.argv)  # Передаём Django команду, например runserver или migrate | execute_from_command_line — передаёт аргументы терминала системе команд Django.
