from datetime import date  # работа с датами

from django.core.management.base import BaseCommand  # основа команды manage.py
from django.db import transaction  # транзакции базы

from universities.models import University  # таблица университетов

VERIFIED_ON = date(2026, 10, 22)  # дата проверки источников

NU_NOTE = (  # пояснение для Nazarbayev University
    "Платный Regular Admission: IELTS 6.0 (Writing 6.0, остальные секции 5.5); "  # условия приёма
    "GPA 4.0/5 — один из академических вариантов. Обучение 2026/27: 15 000 USD без проживания. "  # GPA и стоимость
    "Грантовый конкурс имеет другие условия и здесь не оценивается."  # про гранты
)  # конец текста
GPA_NOTE = (  # пояснение про GPA в США
    "Официальный академический вариант: GPA 2.6/4 или альтернативные ACT/SAT. "  # исходное требование
    "Порог сайта 3.25/5 получен пропорцией 2.6 × 5 / 4; "  # как получили 3.25
    "это условная нормализация для сравнения, не официальная эквивалентность аттестата."  # это условное значение
)  # конец текста
USD_NOTE = (  # пояснение для University of South Dakota
    "IELTS 6.0. Текущая опубликованная оценка Tuition & Fees: 13 616 USD за 30 кредитов в год, "  # IELTS и стоимость
    "без проживания и прочих расходов. Есть конкурсные стипендии."  # что не входит
)  # конец текста
DSU_NOTE = (  # пояснение для Dakota State University
    "IELTS 6.0, каждая секция от 5.5. Tuition & Fees 2026/27 для non-SD residents: "  # IELTS и тариф
    "12 569 USD за 30 кредитов; проживание, оборудование и отдельные предметные сборы не включены. "  # стоимость и что не входит
    "Стипендии зависят от условий отбора."  # про стипендии
)  # конец текста

NU = {"country": "Казахстан", "city": "Астана", "ielts": 6.0, "gpa": 4.0, "tuition": 15000, "scholarship": False}  # общие условия Nazarbayev University
USD = {"country": "США", "city": "Вермиллион", "ielts": 6.0, "gpa": 3.25, "tuition": 13616, "scholarship": True}  # общие условия University of South Dakota
DSU = {"country": "США", "city": "Мэдисон", "ielts": 6.0, "gpa": 3.25, "tuition": 12569, "scholarship": True}  # общие условия Dakota State University
NU_URL = "https://apply.nu.edu.kz/en/engineering"  # официальная ссылка NU

PROGRAMS = [  # список из семи программ
    {  # первая программа
        **NU,  # подставляем общие условия NU
        "name": "Nazarbayev University · Civil and Environmental Engineering",  # название
        "major": "engineering",  # специальность
        "description": f"Civil and Environmental Engineering, бакалавриат. {NU_NOTE}",  # описание
        "source_url": NU_URL,  # официальная ссылка
    },  # конец программы
    {  # вторая программа
        **NU,  # подставляем общие условия NU
        "name": "Nazarbayev University · Electrical and Computer Engineering",  # название
        "major": "engineering",  # специальность
        "description": f"Electrical and Computer Engineering, бакалавриат. {NU_NOTE}",  # описание
        "source_url": NU_URL,  # официальная ссылка
    },  # конец программы
    {  # третья программа
        **NU,  # подставляем общие условия NU
        "name": "Nazarbayev University · Mechanical and Aerospace Engineering",  # название
        "major": "engineering",  # специальность
        "description": f"Mechanical and Aerospace Engineering, бакалавриат. {NU_NOTE}",  # описание
        "source_url": NU_URL,  # официальная ссылка
    },  # конец программы
    {  # четвёртая программа
        **USD,  # подставляем общие условия USD
        "name": "University of South Dakota · Computer Science",  # название
        "major": "cs",  # специальность
        "description": f"Computer Science, бакалавриат. {GPA_NOTE} {USD_NOTE}",  # описание
        "source_url": "https://www.usd.edu/Academics/Undergraduate-Programs/Computer-Science",  # официальная ссылка
    },  # конец программы
    {  # пятая программа
        **USD,  # подставляем общие условия USD
        "name": "University of South Dakota · Business Administration",  # название
        "major": "business",  # специальность
        "description": (  # описание из двух частей
            f"Business Administration, бакалавриат. {GPA_NOTE} {USD_NOTE} "  # название и пояснения
            "Школа бизнеса может предъявлять дополнительные требования."  # дополнительное условие
        ),  # конец описания
        "source_url": "https://www.usd.edu/Academics/Undergraduate-Programs/Business-Administration",  # официальная ссылка
    },  # конец программы
    {  # шестая программа
        **DSU,  # подставляем общие условия DSU
        "name": "Dakota State University · Computer Science",  # название
        "major": "cs",  # специальность
        "description": f"Computer Science, BS. {GPA_NOTE} {DSU_NOTE}",  # описание
        "source_url": "https://dsu.edu/programs/computer-science-bs.html",  # официальная ссылка
    },  # конец программы
    {  # седьмая программа
        **DSU,  # подставляем общие условия DSU
        "name": "Dakota State University · Business Administration",  # название
        "major": "business",  # специальность
        "description": f"Business Administration, BBA. {GPA_NOTE} {DSU_NOTE}",  # описание
        "source_url": "https://dsu.edu/programs/business-administration-bba.html",  # официальная ссылка
    },  # конец программы
]  # конец списка


class Command(BaseCommand):  # команда manage.py seed_real
    help = "Добавляет или обновляет 7 реальных программ."  # текст справки

    @transaction.atomic  # сохранить всё или ничего
    def handle(self, *args, **options):  # сама работа команды
        created_count = 0  # счётчик новых записей
        for program in PROGRAMS:  # перебираем программы
            _, created = University.objects.update_or_create(  # обновляем или создаём запись
                name=program["name"],  # ищем по названию
                major=program["major"],  # и по специальности
                defaults={**program, "is_demo": False, "verified_on": VERIFIED_ON},  # что записать
            )  # конец вызова
            created_count += created  # True считается как 1
        updated_count = len(PROGRAMS) - created_count  # сколько записей обновлено
        self.stdout.write(self.style.SUCCESS(  # печатаем итог зелёным
            f"Реальный каталог: {len(PROGRAMS)} программ; новых: {created_count}; обновлено: {updated_count}."  # текст итога
        ))  # конец вызова
