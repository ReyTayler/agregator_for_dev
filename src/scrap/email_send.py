import random
from datetime import date
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from scrap.models import Vacancy


def send_daily_vacancies():
    User = get_user_model()
    users = User.objects.filter(is_send_email=True, city__isnull=False, language__isnull=False)

    for user in users:
        qs = Vacancy.objects.filter(
            city=user.city,
            language=user.language,
            timestamp=date.today()
        )

        vacancies = list(qs)
        if not vacancies:
            continue

        selected_vacancies = random.sample(vacancies, k=min(3, len(vacancies)))

        subject = f"Подборка вакансий ({user.city.name}, {user.language.name})"
        html_message = render_to_string("scrap/vacancy_mail.html", {
            "user": user,
            "vacancies": selected_vacancies,
        })

        send_mail(
            subject=subject,
            message="",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False
        )
