from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password, **kwargs):
        if not email:
            raise ValueError("Email is required!")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **kwargs):
        if not email:
            raise ValueError("Email is required!")

        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True
        kwargs['is_active'] = True

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=100, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()  # указываем нового менеджера

    def __str__(self):
        return self.username