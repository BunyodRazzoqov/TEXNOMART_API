from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.managers import MyUserManager


# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    email: str = models.EmailField(max_length=255, unique=True)
    username: str = models.CharField(max_length=255, null=True, blank=True)
    image: str = models.ImageField(upload_to='users/images/', blank=True, null=True)
    date_of_birth: str = models.DateField(blank=True, null=True, default=datetime.now())
    is_active: bool = models.BooleanField(default=False)
    is_staff: bool = models.BooleanField(default=False)
    is_superuser: bool = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: list = ['username']

    def __str__(self) -> str:
        return self.email
