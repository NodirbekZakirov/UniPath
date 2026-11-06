def calculate_costs(data):  # считает расходы за год
    months = data["months"]  # сколько месяцев проживания
    items = [  # список из четырёх расходов
        {"label": "Обучение", "amount": data["tuition"]},  # обучение уже указано за год
        {"label": "Жильё", "amount": data["housing"] * months},  # аренда за месяц умножается на месяцы
        {"label": "Питание и другие расходы", "amount": data["living"] * months},  # траты за месяц умножаются на месяцы
        {"label": "Перелёты", "amount": data["travel"]},  # перелёты уже указаны за год
    ]  # конец списка
    total = sum(item["amount"] for item in items)  # все расходы вместе
    funding = min(data["scholarship"], total)  # стипендия не больше самих расходов
    needed = total - funding  # сколько платить самому
    balance = data["budget"] - needed  # остаток бюджета, минус значит нехватка
    return {  # отдаём все числа для страницы
        "items": items,  # статьи расходов
        "total": total,  # все расходы
        "funding": funding,  # учтённая стипендия
        "needed": needed,  # сколько платить самому
        "balance": balance,  # остаток бюджета
        "shortfall": max(0, -balance),  # сколько не хватает, минимум 0
        "budget": data["budget"],  # бюджет пользователя
        "months": months,  # месяцы проживания
    }  # конец словаря
