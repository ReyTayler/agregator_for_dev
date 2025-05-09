from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django_apscheduler.models import DjangoJobExecution
import logging

from scrap.run_scraping import main
from scrap.email_send import send_daily_vacancies

logger = logging.getLogger(__name__)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Задача 1: Запуск парсинга вакансий каждые 12 часов
    scheduler.add_job(
        main,
        trigger="interval",
        hours=12,
        id="vacancy_parser",
        replace_existing=True,
        name="Запуск парсинга вакансий",
    )

    # Задача 2: Отправка вакансий пользователям каждые 17 часов
    scheduler.add_job(
        send_daily_vacancies,
        trigger="interval",
        hours=17,
        id="daily_mailing_job",
        replace_existing=True,
        name="Рассылка вакансий",
    )

    register_events(scheduler)
    scheduler.start()
    logger.info("APScheduler запущен")
