from django.shortcuts import render
from .models import Vacancy, City


def main_view(request):
    vacancies = Vacancy.objects.all()

    return render(request=request,
                  template_name='scrap/home.html',
                  context={"object_list": vacancies})
