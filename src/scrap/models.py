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
