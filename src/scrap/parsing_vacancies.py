import requests
from bs4 import BeautifulSoup
from random import choice

domain_habr_career = "https://career.habr.com"
domain_getmatch = "https://getmatch.ru"
url_api_hh = "https://api.hh.ru/vacancies"

# Заголовки, чтобы замаскироваться под браузер
HEADERS = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 "
                      "YaBrowser/25.2.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
    },
]

jobs_info = []
errors_info = []


def get_vacancies_habr(url_page: str):
    global jobs_info
    global errors_info

    response = requests.get(url=url_page, headers=choice(HEADERS))

    if response.status_code == 200:
        soup = BeautifulSoup(markup=response.text, features="html.parser")
        vacancies_div_list = soup.find_all(name="div", class_="vacancy-card")

        if len(vacancies_div_list) > 0:
            for div in vacancies_div_list:
                # Находим div с названием компании и div с названием вакансии
                company_div = div.find(name="div", class_="vacancy-card__company-title")
                title_div = div.find(name="div", class_="vacancy-card__title")

                title = title_div.a.string
                href = title_div.a.get("href")
                company = company_div.a.string

                # Формирование данных о вакансии в JSON-структуру
                job = {
                    "title": title,
                    "url": domain_habr_career + href,
                    "company": company,
                    "description": "Краткое описание не было предоставлено..."
                }

                jobs_info.append(job)

        else:
            error = {
                "Нет вакансий!": {
                    "title": "Поиск не дал результатов",
                    "url": url_page,
                    "description": "Попробуйте изменить условия поиска",
                }
            }

            errors_info.append(error)
    else:
        error = {
            "Запрос выполнен с ошибкой!": {
                "url": url_page,
                "status_code": response.status_code,
            }
        }
        errors_info.append(error)


def get_vacancies_getmatch(url_page: str):
    global jobs_info
    global errors_info

    response = requests.get(url=url_page, headers=choice(HEADERS))

    if response.status_code == 200:
        soup = BeautifulSoup(markup=response.text, features="html.parser")
        vacancies_div = soup.find_all("div", class_="b-vacancy-card")

        if len(vacancies_div) > 0:
            for vacancy in vacancies_div:
                title_div = vacancy.find(name="div", class_="b-vacancy-card-title")
                title = title_div.h3.a.string
                href = title_div.h3.a.get("href")
                company = title_div.h4.a.string

                # Обрабатываем описание. Вычисляем только текст "Что делать:..."
                description_div = vacancy.find(name="div", class_="b-vacancy-card-description")
                descriptions = description_div.find_all(name='p')
                descriptions = [p.get_text() for p in descriptions]

                main_text = str()
                for description in descriptions:
                    if "Что делать:" in description:
                        main_text = description

                # Формирование данных о вакансии в JSON-структуру
                job = {
                    "title": title,
                    "url": domain_getmatch + href,
                    "company": company,
                    "description": main_text
                }

                jobs_info.append(job)

        else:
            error = {
                "Нет вакансий!": {
                    "title": "По такому запросу мы не нашли удовлетворяющих результатов.",
                    "url": url_page,
                }
            }

            errors_info.append(error)
    else:
        error = {
            "Запрос выполнен с ошибкой!": {
                "url": url_page,
                "status_code": response.status_code,
            }
        }
        errors_info.append(error)


def get_vacancies_hh(
        keyword: str = None, salary_from: int = None, only_with_salary=False, area: int = None
):
    params_api = {
        "text": keyword,
        "salary": salary_from,
        "only_with_salary": only_with_salary,
        "per_page": 100,
        "area": area
    }

    params = {key: value for key, value in params_api.items() if value is not None}

    response = requests.get(url=url_api_hh, headers=choice(HEADERS), params=params)

    if response.status_code == 200:
        data = response.json()
        vacancies = data.get("items")

        if len(vacancies) > 0:
            score = 0
            for vacancy in vacancies:
                # Извлекаем данные о названии, компании, URL вакансии и кратком описании
                title = vacancy["name"]
                company = vacancy["employer"]["name"]
                url = vacancy["alternate_url"]
                description = vacancy['snippet']['responsibility']

                job = {"title": title, "url": url, "company": company, "description": description}

                jobs_info.append(job)
        else:
            error = {
                "Нет вакансий!": {
                    "title": "Поиск не дал результатов",
                    "description": "Попробуйте изменить условия поиска",
                }
            }
            errors_info.append(error)
    else:
        error = {"Запрос выполнен с ошибкой!": {"status_code": response.status_code}}
        errors_info.append(error)
