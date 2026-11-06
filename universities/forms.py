from django import forms  # инструменты для форм

from .models import MAJORS, University  # специальности и таблица вузов

DEFAULT_PROFILE = {"ielts": 6.5, "gpa": 4.0, "budget": 15000, "major": "cs", "country": ""}  # стартовые данные абитуриента
DEFAULT_COSTS = {  # стартовые суммы калькулятора
    "tuition": 15000,  # обучение за год
    "months": 12,  # месяцы проживания
    "housing": 500,  # жильё в месяц
    "living": 300,  # питание и траты в месяц
    "travel": 600,  # перелёты за год
    "scholarship": 2000,  # стипендия за год
    "budget": 25000,  # общий бюджет за год
}  # конец словаря


class SearchForm(forms.Form):  # форма подбора университетов
    ielts = forms.FloatField(  # поле IELTS: дробное число
        label="IELTS", min_value=0, max_value=9, widget=forms.NumberInput(attrs={"step": "0.5"})  # подпись, границы 0–9, шаг 0.5
    )  # конец поля
    gpa = forms.FloatField(  # поле GPA: дробное число
        label="GPA · из 5", min_value=0, max_value=5, widget=forms.NumberInput(attrs={"step": "0.1"})  # подпись, границы 0–5, шаг 0.1
    )  # конец поля
    budget = forms.IntegerField(label="Бюджет · USD / год", min_value=0, max_value=1000000)  # бюджет: целое число от 0 до миллиона
    major = forms.ChoiceField(label="Специальность", choices=MAJORS)  # специальность только из списка
    country = forms.ChoiceField(label="Страна", required=False)  # страна, можно не выбирать

    def __init__(self, *args, **kwargs):  # выполняется при создании формы
        super().__init__(*args, **kwargs)  # сначала обычная настройка формы
        countries = University.objects.order_by("country").values_list("country", flat=True).distinct()  # страны из базы без повторов
        self.fields["country"].choices = [("", "Все страны")] + [(c, c) for c in countries]  # «Все страны» плюс страны из базы


class CostForm(forms.Form):  # форма калькулятора расходов
    tuition = forms.IntegerField(label="Обучение за год", min_value=0, max_value=1000000)  # обучение за год
    months = forms.IntegerField(label="Месяцев проживания", min_value=1, max_value=12)  # месяцев проживания: от 1 до 12
    housing = forms.IntegerField(label="Жильё в месяц", min_value=0, max_value=100000)  # жильё в месяц
    living = forms.IntegerField(label="Питание и другие расходы в месяц", min_value=0, max_value=100000)  # питание и траты в месяц
    travel = forms.IntegerField(label="Перелёты за год", min_value=0, max_value=1000000)  # перелёты за год
    scholarship = forms.IntegerField(label="Ожидаемая стипендия за год", min_value=0, max_value=1000000)  # стипендия за год
    budget = forms.IntegerField(label="Ваш общий бюджет на год", min_value=0, max_value=10000000)  # общий бюджет за год
