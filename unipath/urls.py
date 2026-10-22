from django.contrib import admin  # Подключаем встроенную административную панель | from/import подключают указанные имена.
from django.contrib.auth import views as auth_views  # Используем готовые страницы входа и выхода Django | from/import подключают указанные имена.
from django.urls import path  # Импортируем средство описания маршрутов | from/import подключают указанные имена.
from universities import views  # Подключаем обработчики страниц UniPath | from/import подключают указанные имена.
urlpatterns = [  # Сопоставляем адреса браузера с Python-обработчиками.
    path("", views.home, name="home"),  # path(адрес, обработчик, name) создаёт маршрут; пустая строка — главная, views.home — функция без вызова, name="home" — имя ссылки; открывает подбор.
    path("university/<int:pk>/", views.university_detail, name="university"),  # path связывает адрес с views.university_detail; <int:pk> получает числовой ID из URL, name="university" именует ссылку; открывает программу.
    path("saved/", views.saved, name="saved"),  # path связывает /saved/ с функцией views.saved; name="saved" — имя маршрута; открывает личное избранное.
    path("costs/", views.costs, name="costs"),  # path связывает /costs/ с views.costs; name="costs" — имя маршрута; открывает общий калькулятор.
    path("costs/<int:pk>/", views.costs, name="university_costs"),  # path выбирает views.costs; <int:pk> передаёт числовой ID, name="university_costs" — имя ссылки; подставляет цену программы.
    path("save/<int:pk>/", views.save_university, name="save"),  # path выбирает views.save_university; <int:pk> — ID, name="save" — имя маршрута; обработчик изменяет избранное только через POST.
    path("login/", auth_views.LoginView.as_view(), name="login"),  # path создаёт маршрут /login/; auth_views — псевдоним модуля auth.views, LoginView — класс входа, as_view() создаёт вызываемый обработчик, name="login" — имя ссылки; показывает и проверяет вход.
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),  # path создаёт маршрут /logout/; auth_views — псевдоним модуля auth.views, LogoutView — класс выхода, as_view() создаёт вызываемый обработчик, name="logout" — имя ссылки; завершает сеанс через POST.
    path("register/", views.register, name="register"),  # path связывает /register/ с функцией views.register; name="register" — имя маршрута; открывает регистрацию и принимает её данные.
    path("admin/", admin.site.urls),  # path подключает /admin/; admin — модуль админки, site — её объект, urls — набор готовых маршрутов; открывает управление данными.
]  # Завершаем таблицу маршрутов.
