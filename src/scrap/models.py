from django.db import models


class City(models.Model):
    name = models.CharField(max_length=40, verbose_name="Название города")
    slug = models.CharField(max_length=12, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Города"
        verbose_name = "Город"
