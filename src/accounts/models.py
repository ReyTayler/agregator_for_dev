from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import UserManager
from django.db import models


class ScrapUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Отсутствует адрес эл.почты пользователя!")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class ScrapUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Адрес эл.почты",
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    city = models.ForeignKey(to='scrap.City', on_delete=models.SET_NULL, null=True, blank=True)
    language = models.ForeignKey(to='scrap.Lang', on_delete=models.SET_NULL, null=True, blank=True)
    is_send_email = models.BooleanField(default=True)

    objects = ScrapUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
