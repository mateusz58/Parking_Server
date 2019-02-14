
import pytz
import re
from django.db.models import Q, Sum
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
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
                fields = ('code', 'parking','Cost', 'user',
                          'number_of_cars','active')
                read_only_fields = ('code', 'parking','Cost', 'user',
                          'number_of_cars')



class Booking_Serializer(serializers.ModelSerializer):


    class Meta:
                model = Booking
                fields = ('code', 'parking','Cost', 'user','number_of_cars','active',)
                read_only_fields = ('code',)



class Car_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ( 'id','Date_From', 'Date_To', 'registration_plate', 'booking','status')
        read_only_fields = ('booking','Date_From','Date_To','id','registration_plate')


class Car_Serializer_update(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ( 'id','Date_From', 'Date_To', 'registration_plate', 'booking','status')
        read_only_fields = ('booking','Date_From','Date_To','id','registration_plate')

class Car_booking_Serializer(serializers.ModelSerializer):
    booking = Car_Serializer(many=True)
    class Meta:
        model = Booking
        fields =('code', 'parking','Cost', 'user','number_of_cars','booking','Date_From', 'Date_To','active')
        read_only_fields = ('code', 'parking','Cost', 'user','booking')

#
# class Car_booking_Serializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Booking
#         fields =('code', 'parking','Cost', 'user','number_of_cars','booking')
#         read_only_fields = ('code', 'parking','Cost', 'user',)
#
#
#
# class Request_Car_booking_Serializer(WritableNestedModelSerializer):
#     booking = Car_booking_Serializer(many=True)
#
#
#     class Meta:
#         model = Booking
#         fields =('code', 'parking','Cost', 'user','number_of_cars','booking')
#         read_only_fields = ('code', 'parking','Cost', 'user',)
#





