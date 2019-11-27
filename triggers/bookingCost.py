from pages.models import Booking
from users.models import CustomUser


def get_Cost_Custom(self):
    print("TRIGGER BOOKING COST")
    time1 = self.Date_From
    time2 = self.Date_To
    duration = time2 - time1
    duration_in_s = duration.total_seconds()
    hours = divmod(duration_in_s, 3600)[0]
    minutes = divmod(duration_in_s, 60)[0]
    HOURS = float("{0:.2f}".format(hours + ((minutes / 60) - hours)))
    Cost = self.booking.parking.HOUR_COST * HOURS
    Cost = round(Cost, 2)
    return Cost


def trigger_booking_post(self):
    user_id = CustomUser.objects.get(email=str(self.request.user)).id
    Booking.objects.filter(pk=self.booking.id).update(number_of_cars=self.booking.number_of_cars + 1)
    Booking.objects.filter(pk=self.booking.id).update(Cost=get_Cost_Custom(self) + self.booking.Cost)
