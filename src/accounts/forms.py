from django import forms
from django.contrib.auth import get_user_model, authenticate


class UserLoginForm(forms.Form):
    """
    Форма для аутентификации пользователя по email и паролю.
    Использует кастомную модель пользователя, где email является основным идентификатором.
    """

    email = forms.CharField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": ""})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": ""})
    )

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы и сохранение поля self.user для последующего доступа.
        """
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        Основная логика валидации формы:
        - Проверяет наличие пользователя с указанным email.
        - Аутентифицирует пользователя по email и паролю.
        - Проверяет, активен ли аккаунт.
        Если всё в порядке — сохраняет пользователя в self.user.
        """
        cleaned_data = super().clean()  # получаем очищенные данные после валидации отдельных полей
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            User = get_user_model()  # получаем текущую модель пользователя из настроек проекта

            try:
                user_obj = User.objects.get(email=email)  # пытаемся найти пользователя по email
            except User.DoesNotExist:
                raise forms.ValidationError("Пользователь не найден!")

            # Аутентифицируем пользователя (работает, если настроен кастомный backend с email)
            user_auth = authenticate(email=email, password=password)

            if user_auth is None:
                raise forms.ValidationError("Неверный пароль!")

            if not user_auth.is_active:
                raise forms.ValidationError("Аккаунт отключен!")

            # Сохраняем аутентифицированного пользователя для доступа во view
            self.user = user_auth

        return cleaned_data

    def get_user(self):
        """
        Возвращает аутентифицированного пользователя.
        """
        return self.user
