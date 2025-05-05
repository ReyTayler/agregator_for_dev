from django.urls import path
from accounts.views import login_view, logout_view, register_view, account_settings_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('reg/', register_view, name='registration'),
    path('settings/', account_settings_view, name='settings'),
]

