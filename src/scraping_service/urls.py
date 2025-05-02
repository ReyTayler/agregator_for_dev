from django.contrib import admin
from django.urls import path, include
from scrap.views import main_view, vacancies_list_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include(('accounts.urls', 'accounts'))),
    path('vacancies/', vacancies_list_view, name='vacancies'),
    path('', main_view, name='main'),
]
