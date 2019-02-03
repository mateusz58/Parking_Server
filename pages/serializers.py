
import pytz
import re
from django.db.models import Q, Sum
from rest_framework import serializers

from pages.models import Parking, Booking, CustomUser

from datetime import datetime

class Parking_Serializer_Coordinates(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ('x','y')
        read_only_fields = ('id','x','y')


class Parking_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Parking
        fields = ('id', 'parking_name', 'parking_Street', 'parking_City', 'x','y','free_places','HOUR_COST','number_of_places')
        read_only_fields = ('id','x','y','parking_name','parking_City','free_places','parking_Street')


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





class Booking_Serializer(serializers.ModelSerializer):
    # read_only_fields = ('parking', 'Date_From', 'Date_To','user','registration_plate')


    # Date_To = serializers.SerializerMethodField()
    #
    # def get_Date_From(self, obj):
    #         if obj.Date_From!='0':return str(obj.Date_From).replace('Z'," ").replace('+00:00','')
    # def get_Date_To(self, obj):
    #     if obj.Date_To != '0': return str(obj.Date_To).replace('Z', " ").replace('+00:00', '')


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

    def get_Cost_Custom(self, instance):
        time1 = instance.Date_From
        time2 = instance.Date_To
        duration = time2 - time1
        duration_in_s = duration.total_seconds()
        hours = divmod(duration_in_s, 3600)[0]  ## HOURS DURATION
        minutes = divmod(duration_in_s, 60)[0]
        HOURS = float("{0:.2f}".format(hours + ((minutes / 60) - hours)))
        Cost = instance.parking.HOUR_COST * HOURS*instance.number_of_cars
        return Cost
    Cost=serializers.SerializerMethodField(method_name='get_Cost_Custom')

    class Meta:
                model = Booking
                fields = ('code', 'parking', 'Date_From', 'Date_To', 'Cost', 'user', 'registration_plate','status','HOURS','number_of_cars')
                read_only_fields = ('code','Cost','HOURS')








