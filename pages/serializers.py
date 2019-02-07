
import pytz
import re
from django.db.models import Q, Sum
from rest_framework import serializers

from pages.models import Parking, Booking, CustomUser, Car

from datetime import datetime

class Parking_Serializer_Coordinates(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ('x','y')
        read_only_fields = ('id','x','y')


class Parking_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Parking
        fields = ('id', 'parking_name', 'parking_Street', 'parking_City', 'x','y','free_places','HOUR_COST','number_of_places','user_parking')
        read_only_fields = ('id','x','y','parking_name','parking_City','free_places','parking_Street','user_parking')

class User_Serializer(serializers.ModelSerializer):
        class Meta:
            model = CustomUser
            fields = ('email')
            extra_kwargs = {'password': {'write_only': True}}

            def create(self, validated_data):   ###Walidacja hasla
                user = CustomUser(
                    email=validated_data['email'],
                    login=validated_data['login']
                )
                user.set_password(validated_data['password'])
                user.save()
                return user


class User_Serializer_Login_Email(serializers.ModelSerializer):
        class Meta:
            model = CustomUser
            fields = ('__all__')


class Booking_Serializer_delete(serializers.ModelSerializer):

    class Meta:
                model = Booking
                fields = ('code', 'parking', 'Date_From', 'Date_To', 'Cost', 'user', 'registration_plate',
                          'number_of_cars','status')
                read_only_fields = ('code', 'parking', 'Date_From', 'Date_To', 'Cost', 'user',
                          'number_of_cars')



class Booking_Serializer(serializers.ModelSerializer):
    def get_HOURS_custom(self, instance):
        time1 = instance.Date_From
        time2 = instance.Date_To
        duration = time2 - time1
        duration_in_s = duration.total_seconds()
        hours = divmod(duration_in_s, 3600)[0]  ## HOURS DURATION
        minutes = divmod(duration_in_s, 60)[0]
        result=float("{0:.2f}".format(hours+((minutes/60)-hours)))
        return result

    HOURS = serializers.SerializerMethodField(method_name='get_HOURS_custom')

    class Meta:
                model = Booking
                fields = ('code', 'parking', 'Date_From', 'Date_To', 'Cost', 'user', 'registration_plate','number_of_cars','HOURS','status')
                read_only_fields = ('code','Cost','HOURS','status','HOURS')


class Car_Serializer(serializers.ModelSerializer):



    class Meta:
        model = Car
        fields = (
        'Date_From', 'Date_To', 'registration_plate', 'booking','status')
        read_only_fields = ('booking','Date_From')









