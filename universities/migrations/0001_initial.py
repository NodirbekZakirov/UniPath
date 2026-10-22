# Начальная миграция сгенерирована Django; комментарии добавлены для изучения.
import django.core.validators  # Подключаем проверки диапазонов для описания схемы | import подключает модуль по имени.
import django.db.models.deletion  # Подключаем стратегию удаления связанных записей | import подключает модуль по имени.
from django.conf import settings  # Получаем настроенную модель пользователя | from/import подключают указанные имена.
from django.db import migrations, models  # Подключаем операции изменения схемы и типы колонок | from/import подключают указанные имена.
class Migration(migrations.Migration):  # Описываем начальную версию схемы базы данных | class объявляет класс; имя в скобках — родитель, от которого наследуются возможности.
    initial = True  # Помечаем миграцию как первоначальное создание таблиц.
    dependencies = [  # Перечисляем миграции, которые должны выполниться раньше.
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),  # Ожидаем создание стандартной таблицы пользователей | swappable_dependency — задаёт зависимость миграции от выбранной модели пользователя.
    ]  # Завершаем список зависимостей или операций.
    operations = [  # Перечисляем операции создания нашей схемы.
        migrations.CreateModel(  # Начинаем создание новой таблицы по описанию модели | CreateModel — операция миграции, описывающая создание таблицы.
            name='University',  # Даём первой модели имя University.
            fields=[  # Перечисляем колонки создаваемой таблицы.
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # Создаём автоматически назначаемый первичный ключ | BigAutoField — тип автоматически растущего целого ID.
                ('name', models.CharField(max_length=120, verbose_name='Название')),  # Создаём колонку названия вуза | CharField — поле короткого текста; max_length ограничивает длину | max_length — предельная длина текста.
                ('country', models.CharField(max_length=60, verbose_name='Страна')),  # Создаём колонку страны | CharField — поле короткого текста; max_length ограничивает длину | max_length — предельная длина текста.
                ('city', models.CharField(max_length=60, verbose_name='Город')),  # Создаём колонку города | CharField — поле короткого текста; max_length ограничивает длину | max_length — предельная длина текста.
                ('major', models.CharField(choices=[('cs', 'Computer Science'), ('business', 'Business & Management'), ('engineering', 'Engineering')], max_length=20, verbose_name='Программа')),  # Создаём колонку специальности с ограниченным выбором | CharField — поле короткого текста; max_length ограничивает длину | choices — разрешённые варианты, max_length — предельная длина текста.
                ('ielts', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9)], verbose_name='Минимальный IELTS')),  # Создаём колонку минимального IELTS с валидаторами | FloatField — поле дробного числа; min/max или validators задают границы | MinValueValidator — валидатор нижней допустимой границы | MaxValueValidator — валидатор верхней допустимой границы | validators — проверки поля.
                ('gpa', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Минимальный GPA / 5')),  # Создаём колонку GPA по шкале 5 с валидаторами | FloatField — поле дробного числа; min/max или validators задают границы | MinValueValidator — валидатор нижней допустимой границы | MaxValueValidator — валидатор верхней допустимой границы | validators — проверки поля.
                ('tuition', models.PositiveIntegerField(verbose_name='Обучение, USD/год')),  # Создаём колонку неотрицательной стоимости обучения | PositiveIntegerField — поле неотрицательного целого числа, включая ноль.
                ('scholarship', models.BooleanField(default=False, verbose_name='Есть стипендии')),  # Создаём флаг наличия стипендий | BooleanField — поле логического значения True/False | default — значение по умолчанию.
                ('description', models.TextField(max_length=1500, verbose_name='Описание')),  # Создаём текстовое описание | TextField — поле длинного текста | max_length — предельная длина текста.
                ('source_url', models.URLField(blank=True, verbose_name='Официальный источник')),  # Создаём необязательную ссылку на официальный источник | URLField — поле веб-адреса с проверкой формата при валидации | blank — разрешение пустого значения в форме.
                ('verified_on', models.DateField(blank=True, null=True, verbose_name='Дата проверки источника')),  # Создаём необязательную дату проверки сведений | DateField — поле календарной даты; blank разрешает пустую форму, null — NULL в базе | blank — разрешение пустого значения в форме, null — разрешение NULL в базе.
                ('is_demo', models.BooleanField(default=True, verbose_name='Учебный пример')),  # Создаём флаг учебных данных, по умолчанию включённый | BooleanField — поле логического значения True/False | default — значение по умолчанию.
            ],  # Завершаем список полей модели.
        ),  # Завершаем операцию создания таблицы.
        migrations.CreateModel(  # Начинаем создание новой таблицы по описанию модели | CreateModel — операция миграции, описывающая создание таблицы.
            name='SavedUniversity',  # Даём таблице личных связей имя SavedUniversity.
            fields=[  # Перечисляем колонки создаваемой таблицы.
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # Создаём автоматически назначаемый первичный ключ | BigAutoField — тип автоматически растущего целого ID.
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),  # Создаём внешний ключ владельца с удалением его связей | ForeignKey — ссылка на запись другой таблицы; on_delete задаёт поведение при её удалении | on_delete — правило удаления связанных записей.
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='universities.university')),  # Создаём внешний ключ университета с удалением связанных сохранений | ForeignKey — ссылка на запись другой таблицы; on_delete задаёт поведение при её удалении | on_delete — правило удаления связанных записей.
            ],  # Завершаем список полей модели.
            options={  # Настраиваем дополнительные ограничения таблицы.
                'constraints': [models.UniqueConstraint(fields=('user', 'university'), name='unique_user_university')],  # Запрещаем повторение одной пары пользователь–университет | UniqueConstraint — ограничение уникальности указанной пары полей в базе.
            },  # Завершаем дополнительные настройки таблицы.
        ),  # Завершаем операцию создания таблицы.
    ]  # Завершаем список зависимостей или операций.
