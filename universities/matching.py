from .models import University  # таблица университетов


def calculate_match(profile, university):  # считает баллы одного университета
    checks = [  # список из четырёх проверок
        {"label": "IELTS", "weight": 30, "passed": profile["ielts"] >= university.ielts},  # IELTS не ниже требования: 30 баллов
        {"label": "GPA / 5", "weight": 30, "passed": profile["gpa"] >= university.gpa},  # GPA не ниже требования: 30 баллов
        {"label": "Бюджет", "weight": 20, "passed": profile["budget"] >= university.tuition},  # бюджет покрывает обучение: 20 баллов
        {"label": "Специальность", "weight": 20, "passed": profile["major"] == university.major},  # специальность совпала: 20 баллов
    ]  # конец списка
    score = sum(check["weight"] for check in checks if check["passed"])  # складываем баллы выполненных проверок
    return {"university": university, "score": score, "checks": checks}  # вуз, сумма баллов и проверки


def find_matches(profile):  # подбирает все подходящие университеты
    universities = University.objects.all()  # берём все вузы из базы
    if profile.get("country"):  # если страна выбрана
        universities = universities.filter(country=profile["country"])  # оставляем только эту страну
    results = [calculate_match(profile, university) for university in universities]  # считаем баллы для каждого вуза
    return sorted(results, key=lambda result: (-result["score"], result["university"].name))  # сначала больше баллов, потом по названию
