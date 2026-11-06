from io import StringIO  # текст в памяти вместо вывода на экран

from django.contrib.auth.models import User  # таблица пользователей
from django.core.management import call_command  # запуск команд из кода
from django.test import Client, TestCase  # инструменты для тестов

from .costs import calculate_costs  # проверяем расчёт расходов
from .forms import DEFAULT_COSTS, DEFAULT_PROFILE, CostForm, SearchForm  # проверяем формы
from .matching import calculate_match  # проверяем расчёт баллов
from .models import SavedUniversity, University  # наши таблицы


class UniPathTests(TestCase):  # все тесты проекта
    def setUp(self):  # готовим данные перед каждым тестом
        self.uni = University.objects.create(  # создаём тестовый вуз
            name="Test Campus", country="Китай", city="Тест", major="cs",  # его данные
            ielts=6.5, gpa=4, tuition=15000, description="Учебный пример",  # его требования
        )  # конец вызова
        self.user = User.objects.create_user("student", password="StrongStudyPass2026!")  # создаём тестового пользователя

    def seed_catalog(self):  # загружает каталог для теста
        call_command("seed_real", stdout=StringIO())  # запускаем seed_real без вывода

    def test_real_catalog_has_sources_and_is_repeatable(self):  # каталог верный, повтор без дублей
        self.seed_catalog()  # загружаем каталог
        real = University.objects.filter(is_demo=False)  # берём реальные программы
        self.assertEqual(real.count(), 7)  # их должно быть 7
        for university in real:  # проверяем каждую
            self.assertTrue(university.source_url.startswith("https://"))  # ссылка начинается с https
            self.assertIsNotNone(university.verified_on)  # дата проверки заполнена
            university.full_clean()  # все поля проходят проверку
        self.seed_catalog()  # загружаем второй раз
        self.assertEqual(University.objects.filter(is_demo=False).count(), 7)  # всё ещё 7, дублей нет

    def test_real_catalog_keeps_custom_data_and_demo_by_default(self):  # загрузка не удаляет чужие записи
        self.seed_catalog()  # загружаем каталог
        self.assertTrue(University.objects.filter(pk=self.uni.pk).exists())  # тестовый вуз остался

    def test_real_program_page_shows_official_link(self):  # на странице есть официальная ссылка
        self.seed_catalog()  # загружаем каталог
        university = University.objects.filter(is_demo=False).first()  # берём первую реальную программу
        response = self.client.get(f"/university/{university.pk}/")  # открываем её страницу
        self.assertContains(response, university.source_url)  # ссылка есть на странице
        self.assertContains(response, 'rel="noopener noreferrer"')  # внешняя ссылка открывается безопасно

    def test_equal_requirements_give_full_match(self):  # равные значения дают 100 баллов
        self.assertEqual(calculate_match(DEFAULT_PROFILE, self.uni)["score"], 100)  # проверяем сумму баллов

    def test_failed_academics_do_not_become_admission_probability(self):  # считаются только выполненные условия
        result = calculate_match({**DEFAULT_PROFILE, "ielts": 6, "gpa": 3}, self.uni)  # IELTS и GPA ниже требований
        self.assertEqual(result["score"], 40)  # остаётся 40 баллов
        self.assertEqual([item["passed"] for item in result["checks"]], [False, False, True, True])  # проверки совпадают с результатом

    def test_form_rejects_invalid_ranges_and_unknown_choices(self):  # форма отклоняет неверные данные
        cases = [{"ielts": 10}, {"gpa": 6}, {"budget": -1}, {"major": "hacking"}, {"ielts": "nan"}, {"gpa": "inf"}]  # список неверных значений
        for invalid in cases:  # проверяем каждое
            with self.subTest(invalid=invalid):  # отдельный случай в отчёте
                self.assertFalse(SearchForm({**DEFAULT_PROFILE, **invalid}).is_valid())  # форма должна быть с ошибкой

    def test_home_and_detail_render(self):  # страницы открываются
        self.assertContains(self.client.get("/"), "Test Campus")  # вуз есть на главной
        self.assertContains(self.client.get(f"/university/{self.uni.pk}/"), "Test Campus")  # вуз есть на своей странице
        self.assertEqual(self.client.get("/university/99999/").status_code, 404)  # несуществующий вуз даёт 404

    def test_country_filter_and_invalid_form(self):  # фильтр страны и ошибка формы
        response = self.client.get("/", {**DEFAULT_PROFILE, "country": "Китай"})  # подбор по стране
        self.assertEqual(response.context["total"], 1)  # найден один вуз
        response = self.client.get("/", {**DEFAULT_PROFILE, "ielts": 20})  # подбор с неверным IELTS
        self.assertEqual(response.context["total"], 0)  # результатов нет
        self.assertTrue(response.context["form"].errors)  # форма показывает ошибку

    def test_save_requires_login_and_post(self):  # сохранение только после входа и через POST
        self.assertEqual(self.client.post(f"/save/{self.uni.pk}/").status_code, 302)  # гостя отправляет на вход
        self.client.force_login(self.user)  # входим без пароля
        self.assertEqual(self.client.get(f"/save/{self.uni.pk}/").status_code, 405)  # GET-запрос запрещён

    def test_save_duplicate_and_remove_are_safe(self):  # нет дублей, удаление работает
        self.client.force_login(self.user)  # входим без пароля
        for _ in range(2):  # повторяем два раза
            self.client.post(f"/save/{self.uni.pk}/", {"action": "save"})  # сохраняем вуз
        self.assertEqual(SavedUniversity.objects.filter(user=self.user).count(), 1)  # запись только одна
        self.client.post(f"/save/{self.uni.pk}/", {"action": "remove"})  # удаляем вуз
        self.assertFalse(SavedUniversity.objects.filter(user=self.user).exists())  # записи больше нет

    def test_saved_lists_are_private(self):  # чужое избранное недоступно
        other = User.objects.create_user("other", password="AnotherStrongPass!")  # второй пользователь
        SavedUniversity.objects.create(user=other, university=self.uni)  # вуз сохранил только он
        self.client.force_login(self.user)  # входим первым пользователем
        self.assertNotContains(self.client.get("/saved/"), "Test Campus")  # чужой вуз не виден
        self.client.post(f"/save/{self.uni.pk}/", {"action": "remove"})  # пробуем удалить чужое
        self.assertTrue(SavedUniversity.objects.filter(user=other).exists())  # чужая запись осталась

    def test_csrf_blocks_untrusted_post(self):  # CSRF блокирует поддельный запрос
        client = Client(enforce_csrf_checks=True)  # клиент с проверкой CSRF
        client.force_login(self.user)  # входим без пароля
        self.assertEqual(client.post(f"/save/{self.uni.pk}/", {"action": "save"}).status_code, 403)  # запрос без токена запрещён

    def test_registration_login_logout(self):  # регистрация, вход и выход
        password = "PrivateCampus2026!"  # тестовый пароль
        response = self.client.post(  # регистрируемся
            "/register/", {"username": "newstudent", "password1": password, "password2": password}  # адрес и данные формы
        )  # конец вызова
        self.assertEqual(response.status_code, 302)  # после регистрации переход
        self.assertTrue(User.objects.filter(username="newstudent").exists())  # пользователь создан
        self.client.post("/login/", {"username": "newstudent", "password": password})  # входим
        self.assertEqual(self.client.get("/saved/").status_code, 200)  # избранное открывается
        self.client.post("/logout/")  # выходим
        self.assertEqual(self.client.get("/saved/").status_code, 302)  # избранное снова закрыто

    def test_costs_count_monthly_and_annual_payments_once(self):  # годовые суммы не умножаются на месяцы
        result = calculate_costs(DEFAULT_COSTS)  # считаем пример
        self.assertEqual(result["total"], 25200)  # все расходы
        self.assertEqual(result["needed"], 23200)  # сколько платить самому
        self.assertEqual(result["balance"], 1800)  # остаток бюджета

    def test_costs_show_shortfall_and_never_negative_expenses(self):  # нехватка и большая стипендия
        self.assertEqual(calculate_costs({**DEFAULT_COSTS, "budget": 20000})["shortfall"], 3200)  # не хватает 3200
        self.assertEqual(calculate_costs({**DEFAULT_COSTS, "scholarship": 999999})["needed"], 0)  # платить 0, а не меньше нуля

    def test_costs_handle_zero_expenses_and_nine_months(self):  # нули и неполный год
        data = {key: 0 for key in DEFAULT_COSTS}  # все суммы равны нулю
        data["months"] = 9  # девять месяцев
        self.assertEqual(calculate_costs(data)["needed"], 0)  # платить 0
        self.assertEqual(calculate_costs({**DEFAULT_COSTS, "months": 9})["total"], 22800)  # расходы за девять месяцев

    def test_cost_form_rejects_invalid_values(self):  # калькулятор отклоняет неверные суммы
        cases = [{"tuition": -1}, {"months": 0}, {"months": 13}, {"housing": "nan"}, {"budget": ""}]  # список неверных значений
        for invalid in cases:  # проверяем каждое
            with self.subTest(invalid=invalid):  # отдельный случай в отчёте
                self.assertFalse(CostForm({**DEFAULT_COSTS, **invalid}).is_valid())  # форма должна быть с ошибкой

    def test_calculator_is_public_and_prefills_selected_tuition(self):  # калькулятор подставляет цену вуза
        response = self.client.get(f"/costs/{self.uni.pk}/")  # открываем калькулятор вуза
        self.assertEqual(response.status_code, 200)  # страница открылась
        self.assertEqual(response.context["form"].initial["tuition"], self.uni.tuition)  # стоимость подставилась

    def test_calculator_submission_and_invalid_input(self):  # расчёт и неверный ввод
        response = self.client.get("/costs/", DEFAULT_COSTS)  # отправляем верные суммы
        self.assertEqual(response.status_code, 200)  # страница открылась
        self.assertEqual(response.context["result"]["needed"], 23200)  # итог верный
        response = self.client.get("/costs/", {**DEFAULT_COSTS, "months": 13})  # отправляем 13 месяцев
        self.assertIsNone(response.context["result"])  # результата нет
