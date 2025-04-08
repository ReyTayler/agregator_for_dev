from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpRequest
from .models import Vacancy
from .forms import FindVacancyForm


def main_view(request: HttpRequest):
    form = FindVacancyForm()
    return render(
        request=request, template_name="scrap/main.html", context={"form": form}
    )


def vacancies_list_view(request: HttpRequest):
    city = request.GET.get("city")
    lang = request.GET.get("lang")

    form = FindVacancyForm()

    context = {"city": city, "lang": lang, "form": form}

    vacancies = []
    if city or lang:
        filter_for_vacancy = {}
        if city:
            filter_for_vacancy["city__slug"] = city
        if lang:
            filter_for_vacancy["language__slug"] = lang
        vacancies = Vacancy.objects.filter(**filter_for_vacancy)

    paginator = Paginator(vacancies, per_page=14)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context["object_list"] = page_obj
    return render(
        request=request,
        template_name="scrap/vacancies.html",
        context=context,
    )
