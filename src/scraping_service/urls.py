from django.contrib import admin
from django.urls import path, include
from scrap.views import main_view, vacancies_list_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include(('accounts.urls', 'accounts'))),
    path('vacancies/', vacancies_list_view, name='vacancies'),
    path('ai_chat/', include(('ai_chat.urls', 'ai_chat'))),
    path('', main_view, name='main'),
]
