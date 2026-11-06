from django.contrib.auth import views as auth_views  # готовые страницы входа и выхода
from django.urls import path  # создаёт адреса

from . import views  # наши функции страниц

urlpatterns = [  # список адресов приложения
    path("", views.home, name="home"),  # главная: подбор
    path("university/<int:pk>/", views.university_detail, name="university"),  # страница программы по её номеру
    path("saved/", views.saved, name="saved"),  # список сохранённых
    path("save/<int:pk>/", views.save_university, name="save"),  # сохранить или удалить вуз
    path("costs/", views.costs, name="costs"),  # калькулятор
    path("costs/<int:pk>/", views.costs, name="university_costs"),  # калькулятор для конкретной программы
    path("register/", views.register, name="register"),  # регистрация
    path("login/", auth_views.LoginView.as_view(), name="login"),  # вход
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),  # выход
]  # конец списка
