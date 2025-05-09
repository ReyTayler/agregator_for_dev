import re
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib import messages
from scrap.run_scraping import main
from .models import Vacancy
from .forms import FindVacancyForm


def main_view(request: HttpRequest):
    """Главная страница с формой выбора города и языка"""
    form = FindVacancyForm()
    return render(request, "scrap/main.html", {"form": form})


def parse_salary(salary_str: str) -> int:
    """
    Извлекает числовое значение зарплаты из строки.
    Возвращает верхнюю границу диапазона, если указано два значения.

    Примеры:
        "8 300 — 10 100 $/мес на руки" -> 10100
        "383 000 — 585 000 ₽/мес на руки" -> 585000
        "от 300 000 ₽/мес на руки" -> 300000
        "250000–400000 ₽" -> 400000
        "Не указана" -> 0
    """
    if not salary_str or "Не указана" in salary_str:
        return 0

    # Удаляем все символы, кроме цифр, пробелов, дефисов и тире
    cleaned = re.sub(r'[^\d\s–—\-]', '', salary_str)

    # Заменяем все разделители (дефисы, тире) на единый разделитель
    normalized = re.sub(r'[–—\-]', '-', cleaned)

    # Ищем все последовательности цифр (с возможными пробелами между ними)
    numbers = re.findall(r'\d[\d\s]*\d|\d', normalized)

    if not numbers:
        return 0

    # Обрабатываем найденные числа - удаляем пробелы и преобразуем в int
    processed_numbers = []
    for num in numbers:
        # Удаляем все пробелы между цифрами
        num_clean = re.sub(r'\s', '', num)
        processed_numbers.append(int(num_clean))

    # Если два числа (диапазон), возвращаем второе
    if len(processed_numbers) >= 2:
        return processed_numbers[1]

    # Если только одно число
    return processed_numbers[0]


def vacancies_list_view(request: HttpRequest):
    """
        Представление для отображения списка вакансий с возможностью фильтрации.

        Функциональность:
        - Требует авторизации пользователя.
        - Поддерживает фильтрацию по городу (city), языку программирования (lang) и минимальной зарплате (min_salary).
        - Минимальная зарплата указывается в виде строки и очищается от лишних символов.
        - Зарплата вакансий извлекается из строкового поля, используется верхняя граница диапазона.
        - Поддерживает пагинацию по 14 вакансий на страницу.
        - Отображает сообщение, если по фильтру вакансий не найдено.

        Параметры запроса (GET):
        - city: slug города
        - lang: slug языка программирования
        - min_salary: строка с числом, минимальный порог зарплаты

        Возвращает:
        - HTML-шаблон со списком вакансий (scrap/vacancies.html)
        """

    if not request.user.is_authenticated:
        return redirect("accounts:login")

    # Параметры запроса
    city = request.GET.get("city")
    lang = request.GET.get("lang")
    min_salary_raw = request.GET.get("min_salary")
    salary_specified = request.GET.get("salary_specified")

    # Создаём контекст
    context = {"city": city, "lang": lang}

    # Фильтрация по городу и языку
    filters = {}
    if city:
        filters["city__slug"] = city
    if lang:
        filters["language__slug"] = lang

    vacancies = Vacancy.objects.filter(**filters)

    if salary_specified:
        vacancies = [
            vacancy for vacancy in vacancies
            if parse_salary(vacancy.salary) > 0
        ]
    # Фильтрация по зарплате
    if min_salary_raw:
        min_salary_stripped = re.sub(r"\D", "", min_salary_raw)
        min_salary = int(min_salary_stripped) if min_salary_stripped else 0

        vacancies = [
            vacancy for vacancy in vacancies
            if parse_salary(vacancy.salary) >= min_salary
        ]

    if (city or lang or min_salary_raw) and not vacancies:
        messages.info(request, "По вашему запросу вакансии не найдены.")

    # Пагинация
    paginator = Paginator(vacancies, per_page=14)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context["object_list"] = page_obj
    return render(request, "scrap/vacancies.html", context)
