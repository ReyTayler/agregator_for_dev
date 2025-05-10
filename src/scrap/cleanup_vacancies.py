from datetime import date, timedelta
from .models import Vacancy


def delete_old_vacancies():
    cutoff_date = date.today() - timedelta(days=14)
    deleted_count, _ = Vacancy.objects.filter(timestamp__lt=cutoff_date).delete()
    print(f"Удалено {deleted_count} устаревших вакансий")
