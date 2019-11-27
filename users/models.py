from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):
    pass
class CustomUser(AbstractUser):
    def __str__(self):
        return self.username
