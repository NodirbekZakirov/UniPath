import django.core.validators  # проверки минимума и максимума
import django.db.models.deletion  # правила удаления связей
from django.conf import settings  # настройки проекта
from django.db import migrations, models  # инструменты миграций


class Migration(migrations.Migration):  # первая версия базы, создана Django

    initial = True  # это самая первая миграция

    dependencies = [  # что должно выполниться раньше
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),  # таблица пользователей
    ]  # конец списка

    operations = [  # что сделать с базой
        migrations.CreateModel(  # создать таблицу
            name='University',  # таблица университетов
            fields=[  # её колонки
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # номер записи
                ('name', models.CharField(max_length=120, verbose_name='Название')),  # название
                ('country', models.CharField(max_length=60, verbose_name='Страна')),  # страна
                ('city', models.CharField(max_length=60, verbose_name='Город')),  # город
                ('major', models.CharField(choices=[('cs', 'Computer Science'), ('business', 'Business & Management'), ('engineering', 'Engineering')], max_length=20, verbose_name='Программа')),  # специальность
                ('ielts', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9)], verbose_name='Минимальный IELTS')),  # минимальный IELTS
                ('gpa', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Минимальный GPA / 5')),  # минимальный GPA
                ('tuition', models.PositiveIntegerField(verbose_name='Обучение, USD/год')),  # стоимость обучения
                ('scholarship', models.BooleanField(default=False, verbose_name='Есть стипендии')),  # есть ли стипендии
                ('description', models.TextField(max_length=1500, verbose_name='Описание')),  # описание
                ('source_url', models.URLField(blank=True, verbose_name='Официальный источник')),  # официальная ссылка
                ('verified_on', models.DateField(blank=True, null=True, verbose_name='Дата проверки источника')),  # дата проверки
                ('is_demo', models.BooleanField(default=True, verbose_name='Учебный пример')),  # учебная запись или нет
            ],  # конец колонок
        ),  # конец таблицы
        migrations.CreateModel(  # создать таблицу
            name='SavedUniversity',  # таблица сохранений
            fields=[  # её колонки
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # номер записи
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),  # пользователь
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='universities.university')),  # университет
            ],  # конец колонок
            options={  # дополнительные настройки
                'constraints': [models.UniqueConstraint(fields=('user', 'university'), name='unique_user_university')],  # нельзя сохранить вуз дважды
            },  # конец настроек
        ),  # конец таблицы
    ]  # конец списка
