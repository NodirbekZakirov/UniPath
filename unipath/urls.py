from django.contrib import admin  # встроенная админка
from django.urls import include, path  # path создаёт адрес, include подключает файл с адресами

urlpatterns = [  # главный список адресов сайта
    path("admin/", admin.site.urls),  # адреса админки
    path("", include("universities.urls")),  # остальные адреса в приложении universities
]  # конец списка
