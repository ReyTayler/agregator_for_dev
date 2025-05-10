import django
import os
from django.db import DatabaseError
from django.contrib.auth import get_user_model
import asyncio

# Настройка Django
#os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"
#django.setup()

from scrap.parsing_vacancies import (
    get_vacancies_hh,
    get_vacancies_habr,
    get_vacancies_getmatch,
    jobs_info,
    errors_info
)
from scrap.models import Vacancy, Error, Url

# Парсеры
STANDARD_PARSERS = (
    (get_vacancies_getmatch, "getmatch"),  # Стандартные парсеры на BeautifulSoup
    (get_vacancies_habr, "habr")
)
API_PARSERS = ((get_vacancies_hh, "hh"),)  # Парсеры, работающие через API

# Модель пользователя
User = get_user_model()


async def process_vacancies(loop, values):
    """Запускает парсеры вакансии в отдельных потоках.

    Args:
        loop: Цикл событий asyncio
        values (tuple): Кортеж с функцией парсера, URL, городом и языком программирования
    """
    func, url, city, language = values
    if isinstance(url, dict):
        await loop.run_in_executor(None, lambda: func(**url, city=city, language=language))
    else:
        await loop.run_in_executor(None, lambda: func(url, city=city, language=language))


def get_user_preferences():
    """Получает уникальные пары город-язык от пользователей, разрешивших email-рассылку

    Returns:
        set: Множество кортежей (city_id, language_id)
    """
    users = User.objects.filter(is_send_email=True).values("city_id", "language_id")
    return {(user["city_id"], user["language_id"]) for user in users}


def get_urls_for_users(user_preferences):
    """
    Возвращает список URL-адресов вакансий для каждой уникальной пары (город, язык)
    из предпочтений пользователей.

    Args:
        user_preferences (set): Множество кортежей (city_id, language_id)

    Returns:
        list: Список словарей вида {"city": city_id, "language": language_id, "urls": [...]}
    """
    # Загружаем все URL из базы и создаём сопоставление (city_id, language_id) -> urls
    all_urls = Url.objects.all().values()
    url_mapping = {
        (item["city_id"], item["language_id"]): item["urls"]
        for item in all_urls
    }

    urls_for_users = []
    for city_id, language_id in user_preferences:
        urls = url_mapping.get((city_id, language_id))
        if urls:
            urls_for_users.append({
                "city": city_id,
                "language": language_id,
                "urls": urls,
            })

    return urls_for_users


def save_vacancies():
    """Собирает собранные вакансии в БД"""
    for vacancy in jobs_info:
        try:
            Vacancy(**vacancy).save()
        except DatabaseError:
            continue  # Пропускаем вакансии, которые не удалось сохранить


def save_errors():
    """Сохраняет все пойманные ошибки парсинга в БД"""
    if errors_info:
        for error in errors_info:
            Error(description_error=error).save()


def prepare_tasks(urls_data):
    """Подготавливаем задачи для всех парсеров

    Args:
        urls_data (list): Данные о URL для парсинга

    Returns:
        list: Список задач для выполнения
    """
    tasks = []

    for data in urls_data:
        for parser, site_name in STANDARD_PARSERS:
            url = data["urls"][site_name]
            tasks.append((parser, url, data["city"], data["language"]))

        for parser, name_site in API_PARSERS:
            url = data["urls"][name_site]
            tasks.append((parser, url, data["city"], data["language"]))

    return tasks


def run_tasks(tasks):
    """Запускает асинхронные задачи парсинга

    Args:
        tasks (list): Список подготовленных задач для выполнения
    """
    loop = asyncio.new_event_loop()
    coroutine = [loop.create_task(process_vacancies(loop, task)) for task in tasks]
    loop.run_until_complete(asyncio.wait(coroutine))
    loop.close()


def main():
    """Основной рабочий процесс парсинга вакансий"""

    # Получаем необходимые данные
    user_preferences = get_user_preferences()
    urls_data = get_urls_for_users(user_preferences)

    if urls_data == []:
        return

    # Подготавливаем и запускаем асинхронные задачи
    tasks = prepare_tasks(urls_data)
    run_tasks(tasks)

    # Сохраняем результаты работы парсеров
    save_vacancies()
    save_errors()
