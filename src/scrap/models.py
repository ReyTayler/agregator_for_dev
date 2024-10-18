from django.db import models
from pytils.translit import slugify


class City(models.Model):
    name = models.CharField(max_length=40, verbose_name="Название города", unique=True)
    slug = models.CharField(max_length=12, blank=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Города"
        verbose_name = "Город"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Lang(models.Model):
    name = models.CharField(max_length=40, verbose_name="Язык программирования", unique=True)
    slug = models.CharField(max_length=12, blank=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Языки программирования"
        verbose_name = "Язык программирования"


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=200, verbose_name="Заголовок вакансии")
    company = models.CharField(max_length=100, verbose_name="Работодатель")
    description = models.TextField(verbose_name="Описание")
    city = models.ForeignKey("City", on_delete=models.CASCADE, verbose_name="Город")
    language = models.ForeignKey("Lang", on_delete=models.CASCADE, verbose_name="Язык программирования")
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
