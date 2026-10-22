import os  # Читаем настройки из окружения при необходимости | import подключает модуль по имени.
from pathlib import Path  # Работаем с путями одинаково на Windows и Linux | from/import подключают указанные имена.
BASE_DIR = Path(__file__).resolve().parent.parent  # Находим папку, в которой лежит manage.py | resolve — получает полный нормализованный путь | Path — объект для составления путей к файлам и папкам.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "local-study-only-unipath-change-before-hosting")  # Учебный ключ для локального запуска; серверу нужен собственный ключ | get — читает переменную окружения; второй аргумент — запасное значение.
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"  # По умолчанию включаем удобный локальный режим разработки | get — читает переменную окружения; второй аргумент — запасное значение.
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,testserver").split(",")  # Разрешаем только перечисленные имена сервера | split — разделяет строку по указанному разделителю | get — читает переменную окружения; второй аргумент — запасное значение.
INSTALLED_APPS = ["django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes", "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles", "universities"]  # Подключаем стандартные приложения и нашу логику университетов.
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware", "django.contrib.sessions.middleware.SessionMiddleware", "django.middleware.common.CommonMiddleware", "django.middleware.csrf.CsrfViewMiddleware", "django.contrib.auth.middleware.AuthenticationMiddleware", "django.contrib.messages.middleware.MessageMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware"]  # Обрабатываем безопасность, сессии, CSRF, пользователей и сообщения.
ROOT_URLCONF = "unipath.urls"  # Указываем файл с маршрутами сайта.
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [BASE_DIR / "templates"], "APP_DIRS": True, "OPTIONS": {"context_processors": ["django.template.context_processors.request", "django.contrib.auth.context_processors.auth", "django.contrib.messages.context_processors.messages"]}}]  # Настраиваем HTML-шаблоны и доступ к request, user и messages.
WSGI_APPLICATION = "unipath.wsgi.application"  # Указываем точку входа для обычного Python-веб-сервера.
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}  # Храним данные в одном файле SQLite.
AUTH_PASSWORD_VALIDATORS = [{"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"}, {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"}, {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"}, {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"}]  # Проверяем сложность паролей стандартными средствами Django.
LANGUAGE_CODE = "ru"  # Показываем встроенные формы и ошибки на русском языке.
TIME_ZONE = "Asia/Tashkent"  # Используем часовой пояс Ташкента.
USE_I18N = True  # Включаем переводы сообщений Django.
USE_TZ = True  # Храним время с информацией о часовом поясе.
STATIC_URL = "static/"  # Задаём адреса CSS и других статических файлов.
STATICFILES_DIRS = [BASE_DIR / "static"]  # Указываем папку нашего CSS.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"  # Автоматически создаём числовые идентификаторы записей.
LOGIN_URL = "login"  # Отправляем неавторизованных пользователей на страницу входа.
LOGIN_REDIRECT_URL = "saved"  # После входа открываем сохранённые университеты.
LOGOUT_REDIRECT_URL = "home"  # После выхода возвращаем на подбор.
