from django import forms
from .models import City, Lang


class FindVacancyForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  required=False,
                                  to_field_name="slug",
                                  widget=forms.Select(attrs={"class": "form-select"}),
                                  label="Город:")

    lang = forms.ModelChoiceField(queryset=Lang.objects.all(),
                                  required=False,
                                  to_field_name="slug",
                                  widget=forms.Select(attrs={"class": "form-select"}),
                                  label="Язык программирования:")
