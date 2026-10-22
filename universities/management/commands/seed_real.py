from datetime import date  # date — тип календарной даты; фиксируем день ручной проверки источников, а не запуска команды.
from django.core.management.base import BaseCommand  # BaseCommand — основа команды manage.py; Django вызывает её метод handle.
from django.db import transaction  # transaction управляет изменениями базы; atomic отменяет весь импорт при ошибке.
from universities.models import University  # University — модель одной программы; objects предоставляет методы работы с таблицей.
VERIFIED_ON = date(2026, 10, 22)  # date(год, месяц, день) создаёт дату проверки; все ссылки приведены в SOURCES.md.
NU_NOTE = "Платный Regular Admission: IELTS 6.0 (Writing 6.0, остальные секции 5.5); GPA 4.0/5 — один из академических вариантов. Обучение 2026/27: 15 000 USD без проживания. Грантовый конкурс имеет другие условия и здесь не оценивается."  # Общие исходные условия выбранного платного маршрута NU.
GPA_NOTE = "Официальный академический вариант: GPA 2.6/4 или альтернативные ACT/SAT. Порог сайта 3.25/5 получен пропорцией 2.6 × 5 / 4; это условная нормализация для сравнения, не официальная эквивалентность аттестата."  # Открыто отличаем данные источника от существующей пятибалльной шкалы проекта.
USD_NOTE = "IELTS 6.0. Текущая опубликованная оценка Tuition & Fees: 13 616 USD за 30 кредитов в год, без проживания и прочих расходов. Есть конкурсные стипендии."  # Тариф USD взят из текущей официальной таблицы, которая не подписывает его учебным годом.
DSU_NOTE = "IELTS 6.0, каждая секция от 5.5. Tuition & Fees 2026/27 для non-SD residents: 12 569 USD за 30 кредитов; проживание, оборудование и отдельные предметные сборы не включены. Стипендии зависят от условий отбора."  # Используем официальный ориентир DSU, а не полный счёт конкретного студента.
PROGRAMS = [  # Список словарей; каждый словарь соответствует отдельной программе реально существующего вуза.
    {  # Начинаем запись первой инженерной программы.
        "name": "Nazarbayev University · Civil and Environmental Engineering", "major": "engineering",  # name — вуз и программа; major — прежняя категория алгоритма.
        "country": "Казахстан", "city": "Астана", "ielts": 6.0, "gpa": 4.0, "tuition": 15000, "scholarship": False,  # Порог уже опубликован по шкале 5; грант не относится к выбранному платному маршруту.
        "description": "Civil and Environmental Engineering, бакалавриат. " + NU_NOTE,  # + соединяет описание программы с проверенными общими условиями.
        "source_url": "https://apply.nu.edu.kz/en/engineering",  # source_url — официальная страница программы, доступная по ссылке в существующей карточке.
    },  # Завершаем первую программу.
    {  # Начинаем вторую инженерную программу.
        "name": "Nazarbayev University · Electrical and Computer Engineering", "major": "engineering",  # Различаем программы по названию, сохраняя общий код engineering.
        "country": "Казахстан", "city": "Астана", "ielts": 6.0, "gpa": 4.0, "tuition": 15000, "scholarship": False,  # Общий платный приём NU и годовая цена обучения 2026/27 в USD.
        "description": "Electrical and Computer Engineering, бакалавриат. " + NU_NOTE,  # Добавляем исходные академические условия и сведения о цене.
        "source_url": "https://apply.nu.edu.kz/en/engineering",  # Официальная страница включает именно эту программу бакалавриата.
    },  # Завершаем вторую программу.
    {  # Начинаем третью инженерную программу.
        "name": "Nazarbayev University · Mechanical and Aerospace Engineering", "major": "engineering",  # Сохраняем настоящее название программы.
        "country": "Казахстан", "city": "Астана", "ielts": 6.0, "gpa": 4.0, "tuition": 15000, "scholarship": False,  # Стоимость не включает проживание и не обещает грантовое финансирование.
        "description": "Mechanical and Aerospace Engineering, бакалавриат. " + NU_NOTE,  # Соединяем название с условиями выбранного варианта поступления.
        "source_url": "https://apply.nu.edu.kz/en/engineering",  # Ссылка открывает официальное описание инженерных направлений NU.
    },  # Завершаем третью программу.
    {  # Начинаем программу University of South Dakota.
        "name": "University of South Dakota · Computer Science", "major": "cs",  # cs — существующая категория Computer Science.
        "country": "США", "city": "Вермиллион", "ielts": 6.0, "gpa": 3.25, "tuition": 13616, "scholarship": True,  # 3.25/5 — условное представление официальных 2.6/4, явно объяснённое ниже.
        "description": "Computer Science, бакалавриат. " + GPA_NOTE + " " + USD_NOTE,  # Указываем исходную шкалу, ограничения нормализации и состав стоимости.
        "source_url": "https://www.usd.edu/Academics/Undergraduate-Programs/Computer-Science",  # Прямой официальный адрес программы.
    },  # Завершаем Computer Science в USD.
    {  # Начинаем бизнес-программу того же университета.
        "name": "University of South Dakota · Business Administration", "major": "business",  # business — прежняя категория Business & Management.
        "country": "США", "city": "Вермиллион", "ielts": 6.0, "gpa": 3.25, "tuition": 13616, "scholarship": True,  # Используем общие условия первичного приёма международных абитуриентов.
        "description": "Business Administration, бакалавриат. " + GPA_NOTE + " " + USD_NOTE + " Школа бизнеса может предъявлять дополнительные требования.",  # Не выдаём общий приём в университет за выполнение всех требований школы бизнеса.
        "source_url": "https://www.usd.edu/Academics/Undergraduate-Programs/Business-Administration",  # Ссылка на официальную программу BBA.
    },  # Завершаем бизнес-программу USD.
    {  # Начинаем программу Dakota State University, отдельного университета в Мэдисоне.
        "name": "Dakota State University · Computer Science", "major": "cs",  # Настоящее название и прежняя категория cs.
        "country": "США", "city": "Мэдисон", "ielts": 6.0, "gpa": 3.25, "tuition": 12569, "scholarship": True,  # Используем общие требования DSU и оценку обучения для non-SD residents.
        "description": "Computer Science, BS. " + GPA_NOTE + " " + DSU_NOTE,  # Поясняем источник GPA, секции IELTS и исключённые расходы.
        "source_url": "https://dsu.edu/programs/computer-science-bs.html",  # Прямая ссылка на официальный бакалавриат Computer Science.
    },  # Завершаем программу DSU Computer Science.
    {  # Начинаем последнюю программу каталога.
        "name": "Dakota State University · Business Administration", "major": "business",  # Название соответствует официальному BBA.
        "country": "США", "city": "Мэдисон", "ielts": 6.0, "gpa": 3.25, "tuition": 12569, "scholarship": True,  # Сохраняем сопоставимые условия первичного приёма и опубликованный годовой ориентир.
        "description": "Business Administration, BBA. " + GPA_NOTE + " " + DSU_NOTE,  # Все ограничения источников остаются видны в описании карточки.
        "source_url": "https://dsu.edu/programs/business-administration-bba.html",  # Официальная страница бизнес-программы DSU.
    },  # Завершаем последнюю запись.
]  # Закрываем список семи программ трёх университетов.
LEGACY_CAMPUSES = ("Aster University", "Cedar Institute", "Northstar College", "Maplebridge University", "Elmridge Institute", "Harbourfield University", "Linden University", "Silverbrook College", "Redwood University", "Juniper Institute")  # Точные имена старых вымышленных кампусов нужны только для адресной очистки.
class Command(BaseCommand):  # class объявляет класс; BaseCommand подключает его к системе команд Django.
    help = "Добавляет или обновляет 7 реальных программ; --replace-demo удаляет только стандартные старые примеры."  # help — текст встроенной справки manage.py help seed_real.
    def add_arguments(self, parser):  # add_arguments настраивает параметры команды; parser — обработчик аргументов командной строки.
        parser.add_argument("--replace-demo", action="store_true", help="Удалить стандартные вымышленные записи и их сохранения.")  # add_argument объявляет флаг; store_true означает True при наличии флага и False без него.
    @transaction.atomic  # atomic — декоратор транзакции: сохраняем весь импорт целиком либо отменяем его при ошибке.
    def handle(self, *args, **options):  # handle выполняет команду; self — текущий объект, args — позиционные аргументы, options — именованные настройки.
        removed = 0  # Число удалённых университетских записей, без каскадных сохранений.
        if options["replace_demo"]:  # if запускает очистку только при явно переданном --replace-demo.
            legacy_names = [f"{name} · {major}" for name in LEGACY_CAMPUSES for major in ("CS", "BUSINESS", "ENGINEERING")]  # Два for строят 30 точных старых имён; f-строка подставляет значения.
            legacy = University.objects.filter(name__in=legacy_names, is_demo=True, source_url="")  # filter ограничивает выборку; __in означает имя из списка; пользовательские и подтверждённые записи не выбираются.
            removed = legacy.count()  # count подсчитывает выбранные программы до удаления.
            legacy.delete()  # delete удаляет выбранные примеры и их личные сохранения по правилу CASCADE модели.
        created_count = 0  # Начинаем счётчик новых реальных программ.
        for program in PROGRAMS:  # for последовательно берёт каждый словарь программы.
            fields = {**program, "is_demo": False, "verified_on": VERIFIED_ON}  # ** раскрывает словарь; дополняем его статусом реальных данных и датой проверки.
            name = fields.pop("name")  # pop получает название и удаляет ключ из словаря остальных полей.
            major = fields.pop("major")  # Извлекаем второй ключ поиска, чтобы повторная загрузка находила ту же программу.
            _, created = University.objects.update_or_create(name=name, major=major, defaults=fields)  # update_or_create обновляет запись или создаёт новую; результат — объект и флаг created, объект здесь не нужен (_).
            created_count += int(created)  # int переводит True в 1 и False в 0; += прибавляет количество новых записей.
        self.stdout.write(self.style.SUCCESS(f"Реальный каталог: {len(PROGRAMS)} программ; новых: {created_count}; обновлено: {len(PROGRAMS) - created_count}; удалено старых примеров: {removed}."))  # len считает элементы; SUCCESS оформляет сообщение, write печатает его в терминал.
