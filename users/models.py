from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class CustomUserManager(UserManager):
    pass



class CustomUser(AbstractUser):

    # objects = CustomUserManager()

    def __str__(self):
        return self.username



    permissions = (("Client", "Send POST request to booking API"),
                       ("Client", "Send POST request to rest-auth/registration/"),
                       ("Client", "Send POST request to rest-auth/login/"),
                       ("Client", "Send GET request to booking API"),
                       ("Client", "Send GET request to Parking API"),
                       ("Client", "Send GET request to Users API"),
                       ("Parking manager", "View booking reservation [only for chosen parkings]"),
                       ("Parking manager", "Send POST request to booking API"),
                       ("Parking manager", "Trip to Dehradoon"))
