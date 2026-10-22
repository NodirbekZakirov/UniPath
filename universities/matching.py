def calculate_match(profile, university):  # Сравниваем профиль с четырьмя учебными критериями программы | def объявляет функцию/метод; profile — словарь пользователя, university — объект программы; возвращает словарь university/score/checks.
    checks = [  # Собираем объяснения, баллы и результат каждого сравнения в один список.
        {"label": "IELTS", "weight": 30, "passed": profile["ielts"] >= university.ielts, "value": university.ielts},  # Даём 30 баллов, если IELTS не ниже указанного минимума.
        {"label": "GPA / 5", "weight": 30, "passed": profile["gpa"] >= university.gpa, "value": university.gpa},  # Даём 30 баллов за соответствие среднему баллу по шкале 5.
        {"label": "Бюджет", "weight": 20, "passed": profile["budget"] >= university.tuition, "value": f"${university.tuition:,} / год"},  # Даём 20 баллов, если годовая стоимость укладывается в бюджет.
        {"label": "Специальность", "weight": 20, "passed": profile["major"] == university.major, "value": university.get_major_display()},  # Даём 20 баллов за совпадение выбранной программы | get_major_display — метод Django: возвращает подпись choices вместо кода специальности.
    ]  # Завершаем список критериев.
    score = sum(check["weight"] for check in checks if check["passed"])  # Складываем веса только выполненных критериев, максимум 100 | sum — складывает числа из перебираемой последовательности.
    return {"university": university, "score": score, "checks": checks}  # Возвращаем вуз, оценку и объяснения для карточки | return завершает вызов и отдаёт результат вызывающему коду.
