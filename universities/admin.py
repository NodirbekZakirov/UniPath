from django import forms  # инструменты для форм
from django.contrib import admin  # встроенная админка
from django.core.exceptions import ValidationError  # ошибка проверки формы

from .models import SavedUniversity, University  # наши таблицы

admin.site.site_header = "UniPath · управление"  # заголовок админки
admin.site.site_title = "UniPath Admin"  # название вкладки
admin.site.register(SavedUniversity)  # показываем сохранения в админке


class UniversityAdminForm(forms.ModelForm):  # форма вуза в админке
    class Meta:  # настройки формы
        model = University  # таблица университетов
        fields = "__all__"  # показываем все поля

    def clean(self):  # дополнительная проверка формы
        data = super().clean()  # сначала обычная проверка
        if not data.get("is_demo", True) and not (data.get("source_url") and data.get("verified_on")):  # реальному вузу нужны ссылка и дата
            raise ValidationError("Для реального вуза укажите официальный источник и дату его проверки.")  # показываем ошибку
        return data  # возвращаем проверенные данные


@admin.register(University)  # подключаем вузы к админке
class UniversityAdmin(admin.ModelAdmin):  # настройки списка вузов
    form = UniversityAdminForm  # используем форму выше
    list_display = ("name", "country", "major", "ielts", "gpa", "tuition", "is_demo")  # колонки в списке
    list_filter = ("country", "major", "is_demo")  # фильтры справа
    search_fields = ("name", "city")  # поиск по названию и городу
