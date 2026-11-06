import os  # читаем настройки системы
from pathlib import Path  # удобная работа с путями

BASE_DIR = Path(__file__).resolve().parent.parent  # папка, где лежит manage.py

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "local-study-only-unipath-change-before-hosting")  # секретный ключ Django
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"  # режим разработки включён по умолчанию
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,testserver").split(",")  # на каких адресах работает сайт

INSTALLED_APPS = [  # подключённые приложения
    "django.contrib.admin",  # админка
    "django.contrib.auth",  # пользователи и вход
    "django.contrib.contenttypes",  # служебные данные о моделях
    "django.contrib.sessions",  # сессии посетителей
    "django.contrib.messages",  # уведомления
    "django.contrib.staticfiles",  # CSS-файлы
    "universities",  # наше приложение
]  # конец списка

MIDDLEWARE = [  # обработчики каждого запроса
    "django.middleware.security.SecurityMiddleware",  # базовая защита
    "django.contrib.sessions.middleware.SessionMiddleware",  # включает сессии
    "django.middleware.common.CommonMiddleware",  # общая обработка запросов
    "django.middleware.csrf.CsrfViewMiddleware",  # защита форм от подделки
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # определяет текущего пользователя
    "django.contrib.messages.middleware.MessageMiddleware",  # включает уведомления
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # запрет встраивания сайта в чужие страницы
]  # конец списка

ROOT_URLCONF = "unipath.urls"  # главный файл адресов
WSGI_APPLICATION = "unipath.wsgi.application"  # точка входа для сервера

TEMPLATES = [  # настройки HTML-шаблонов
    {  # начало настроек
        "BACKEND": "django.template.backends.django.DjangoTemplates",  # система шаблонов Django
        "DIRS": [BASE_DIR / "templates"],  # наша папка с шаблонами
        "APP_DIRS": True,  # искать шаблоны и в приложениях
        "OPTIONS": {  # дополнительные настройки
            "context_processors": [  # что доступно во всех шаблонах
                "django.template.context_processors.request",  # текущий запрос
                "django.contrib.auth.context_processors.auth",  # текущий пользователь
                "django.contrib.messages.context_processors.messages",  # уведомления
            ],  # конец списка
        },  # конец OPTIONS
    },  # конец настроек
]  # конец списка

DATABASES = {  # настройки базы данных
    "default": {  # основная база
        "ENGINE": "django.db.backends.sqlite3",  # используем SQLite
        "NAME": BASE_DIR / "db.sqlite3",  # файл базы данных
    },  # конец настроек базы
}  # конец словаря
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"  # тип автоматического ID

AUTH_PASSWORD_VALIDATORS = [  # правила для паролей
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},  # не похож на логин
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},  # минимальная длина
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},  # не слишком простой
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},  # не только цифры
]  # конец списка
LOGIN_URL = "login"  # куда отправлять гостя
LOGIN_REDIRECT_URL = "saved"  # куда идти после входа
LOGOUT_REDIRECT_URL = "home"  # куда идти после выхода

LANGUAGE_CODE = "ru"  # русский язык
TIME_ZONE = "Asia/Tashkent"  # часовой пояс Ташкента
USE_I18N = True  # включить переводы Django
USE_TZ = True  # учитывать часовые пояса

STATIC_URL = "static/"  # адрес CSS-файлов в браузере
STATICFILES_DIRS = [BASE_DIR / "static"]  # папка с CSS на диске
