from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class CustomUserManager(UserManager):
    pass
class CustomUser(AbstractUser):
    def __str__(self):
        return self.username
