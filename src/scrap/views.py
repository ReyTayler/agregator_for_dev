from django.shortcuts import render
from django.http import HttpRequest
from .models import Vacancy, City
from .forms import FindVacancyForm


def main_view(request: HttpRequest):
    print(request.GET)
    city = request.GET.get('city')
    lang = request.GET.get('lang')

    form = FindVacancyForm()

    vacancies = []
    if city or lang:
        filter_for_vacancy = {}
        if city:
            filter_for_vacancy['city__slug'] = city
        if lang:
            filter_for_vacancy['language__slug'] = lang
        vacancies = Vacancy.objects.filter(**filter_for_vacancy)

    return render(request=request,
                  template_name='scrap/home.html',
                  context={"object_list": vacancies,
                           "form": form})
