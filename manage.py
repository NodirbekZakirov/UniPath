import os  # работа с настройками системы
import sys  # аргументы командной строки

from django.core.management import execute_from_command_line  # запускает команды Django

if __name__ == "__main__":  # только при прямом запуске файла
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unipath.settings")  # указываем файл настроек
    execute_from_command_line(sys.argv)  # выполняем команду, например runserver
