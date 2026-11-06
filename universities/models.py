from django.conf import settings  # настройки проекта
from django.core.validators import MaxValueValidator, MinValueValidator  # проверки минимума и максимума
from django.db import models  # инструменты для таблиц

MAJORS = [  # список специальностей: код и название
    ("cs", "Computer Science"),  # компьютерные науки
    ("business", "Business & Management"),  # бизнес
    ("engineering", "Engineering"),  # инженерия
]  # конец списка


class University(models.Model):  # таблица: одна запись — одна программа вуза
    name = models.CharField("Название", max_length=120)  # название
    country = models.CharField("Страна", max_length=60)  # страна
    city = models.CharField("Город", max_length=60)  # город
    major = models.CharField("Программа", max_length=20, choices=MAJORS)  # специальность из списка MAJORS
    ielts = models.FloatField("Минимальный IELTS", validators=[MinValueValidator(0), MaxValueValidator(9)])  # минимальный IELTS от 0 до 9
    gpa = models.FloatField("Минимальный GPA / 5", validators=[MinValueValidator(0), MaxValueValidator(5)])  # минимальный GPA от 0 до 5
    tuition = models.PositiveIntegerField("Обучение, USD/год")  # стоимость обучения за год в USD
    scholarship = models.BooleanField("Есть стипендии", default=False)  # есть ли стипендии
    description = models.TextField("Описание", max_length=1500)  # описание программы
    source_url = models.URLField("Официальный источник", blank=True)  # ссылка на официальный сайт
    verified_on = models.DateField("Дата проверки источника", null=True, blank=True)  # когда проверили данные
    is_demo = models.BooleanField("Учебный пример", default=True)  # учебная запись или реальная

    def __str__(self):  # как объект подписан в админке
        return self.name  # показываем название


class SavedUniversity(models.Model):  # таблица: кто какой вуз сохранил
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # пользователь, удалится вместе с записью
    university = models.ForeignKey(University, on_delete=models.CASCADE)  # университет, удалится вместе с записью

    class Meta:  # дополнительные настройки таблицы
        constraints = [  # ограничения таблицы
            models.UniqueConstraint(fields=["user", "university"], name="unique_user_university"),  # нельзя сохранить один вуз дважды
        ]  # конец списка
