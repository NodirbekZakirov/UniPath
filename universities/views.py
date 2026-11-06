from django.contrib import messages  # уведомления на странице
from django.contrib.auth.decorators import login_required  # login_required: только для вошедших
from django.contrib.auth.forms import UserCreationForm  # готовая форма регистрации
from django.core.paginator import Paginator  # делит список на страницы
from django.shortcuts import get_object_or_404, redirect, render  # найти запись, перейти, показать страницу
from django.views.decorators.http import require_POST  # require_POST: только POST-запросы

from .costs import calculate_costs  # наш расчёт расходов
from .forms import DEFAULT_COSTS, DEFAULT_PROFILE, CostForm, SearchForm  # наши формы и стартовые значения
from .matching import calculate_match, find_matches  # наш расчёт баллов и подбор
from .models import SavedUniversity, University  # таблицы базы данных

RESULTS_PER_PAGE = 6  # карточек на одной странице


def get_profile(request):  # достаёт данные абитуриента
    return request.session.get("profile", DEFAULT_PROFILE)  # из сессии или стартовый пример


def home(request):  # главная страница с подбором
    profile = get_profile(request)  # последние сохранённые данные
    form = SearchForm(request.GET if "ielts" in request.GET else None, initial=profile)  # заполняем форму, если её отправили
    results = []  # при ошибке список останется пустым
    if not form.is_bound:  # форму ещё не отправляли
        results = find_matches(profile)  # подбор по сохранённым данным
    elif form.is_valid():  # форму отправили без ошибок
        request.session["profile"] = form.cleaned_data  # запоминаем новые данные
        results = find_matches(form.cleaned_data)  # подбор по новым данным

    query = request.GET.copy()  # копия параметров из адреса
    query.pop("page", None)  # убираем старый номер страницы
    saved_ids = set()  # для гостя сохранённых нет
    if request.user.is_authenticated:  # если пользователь вошёл
        saved_ids = set(  # собираем ID его вузов
            SavedUniversity.objects.filter(user=request.user).values_list("university_id", flat=True)  # только его записи
        )  # конец set
    return render(request, "universities/home.html", {  # показываем главную страницу
        "form": form,  # форма
        "page": Paginator(results, RESULTS_PER_PAGE).get_page(request.GET.get("page")),  # карточки текущей страницы
        "total": len(results),  # всего программ
        "query": query.urlencode(),  # фильтры для ссылок страниц
        "saved_ids": saved_ids,  # сохранённые вузы
        "active": "home",  # активный пункт меню
    })  # конец вызова


def university_detail(request, pk):  # страница одной программы
    university = get_object_or_404(University, pk=pk)  # ищем вуз или ошибка 404
    profile = get_profile(request)  # данные абитуриента
    is_saved = (  # сохранил ли пользователь этот вуз
        request.user.is_authenticated  # пользователь вошёл
        and SavedUniversity.objects.filter(user=request.user, university=university).exists()  # и запись есть в базе
    )  # конец условия
    return render(request, "universities/university.html", {  # показываем страницу программы
        "university": university,  # сам вуз
        "result": calculate_match(profile, university),  # баллы и проверки
        "is_saved": is_saved,  # сохранён или нет
        "profile": profile,  # данные абитуриента
    })  # конец вызова


@login_required  # только для вошедших
def saved(request):  # страница сохранённых вузов
    profile = get_profile(request)  # данные абитуриента
    links = SavedUniversity.objects.filter(user=request.user).select_related("university")  # записи пользователя вместе с вузами
    results = [calculate_match(profile, link.university) for link in links]  # считаем баллы для каждого
    return render(request, "universities/saved.html", {"results": results, "active": "saved"})  # показываем список


@login_required  # только для вошедших
@require_POST  # только через форму, не по ссылке
def save_university(request, pk):  # сохраняет или удаляет вуз
    university = get_object_or_404(University, pk=pk)  # ищем вуз или ошибка 404
    if request.POST.get("action") == "remove":  # если нажали «удалить»
        SavedUniversity.objects.filter(user=request.user, university=university).delete()  # удаляем только свою запись
        messages.success(request, "Университет удалён из сохранённых.")  # уведомление об удалении
        return redirect("saved")  # возвращаемся к списку
    SavedUniversity.objects.get_or_create(user=request.user, university=university)  # сохраняем без дублей
    messages.success(request, "Университет сохранён. Вы найдёте его в своём списке.")  # уведомление о сохранении
    return redirect("university", pk=pk)  # возвращаемся на страницу вуза


def register(request):  # страница регистрации
    form = UserCreationForm(request.POST if request.method == "POST" else None)  # заполняем форму, если это POST
    if form.is_valid():  # данные без ошибок
        form.save()  # создаём пользователя
        messages.success(request, "Аккаунт создан. Теперь войдите в UniPath.")  # уведомление об успехе
        return redirect("login")  # переходим ко входу
    return render(request, "registration/register.html", {"form": form})  # показываем форму и ошибки


def costs(request, pk=None):  # страница калькулятора
    university = get_object_or_404(University, pk=pk) if pk is not None else None  # вуз, если указан номер в адресе
    initial = request.session.get("costs", DEFAULT_COSTS).copy()  # прошлые суммы или стартовые
    if university:  # если открыли для конкретного вуза
        initial["tuition"] = university.tuition  # подставляем его стоимость

    form = CostForm(request.GET or None, initial=initial)  # заполняем форму, если её отправили
    result = None  # при ошибке результата не будет
    if not form.is_bound:  # форму ещё не отправляли
        result = calculate_costs(initial)  # считаем по стартовым суммам
    elif form.is_valid():  # форму отправили без ошибок
        request.session["costs"] = form.cleaned_data  # запоминаем суммы
        result = calculate_costs(form.cleaned_data)  # считаем по новым суммам

    return render(request, "universities/costs.html", {  # показываем калькулятор
        "form": form,  # форма
        "result": result,  # результат расчёта
        "university": university,  # выбранный вуз
        "active": "costs",  # активный пункт меню
    })  # конец вызова
