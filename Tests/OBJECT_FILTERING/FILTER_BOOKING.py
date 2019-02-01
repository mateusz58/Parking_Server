
from users.models import CustomUser



from pages.models import Parking, Booking, CustomUser
from django.utils import timezone


## Wyswietlanie wszystkich

Booking.objects.all()

Parking.objects.all()

# queryset =  Booking.objects.all()


print("FILTERED FIELD NAME OF FOREIGN KEY")
# Booking.objects.get(user=1).code
print("FILTERED FIELD EXISTS")
# userfilter(name=group_name).exists()
#
# user.groups.filter(name=group_name).exists()

# CustomUser.objects.filter(email='o8922871@nwytg.net').exists()
print("ID")
CustomUser.objects.get(email='o8922871@nwytg.net').id






