from django.contrib import admin
from .models import City, Lang, Vacancy, Error, Url


class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")


class LangAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")


admin.site.register(City, CityAdmin)
admin.site.register(Lang, LangAdmin)
admin.site.register(Vacancy)
admin.site.register(Error)
admin.site.register(Url)
