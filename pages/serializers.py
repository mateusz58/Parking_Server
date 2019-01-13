import datetime

from rest_framework import serializers

from pages.models import Parking, Booking, CustomUser



class Parking_Serializer_Coordinates(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ('x','y')
        read_only_fields = ('id','x','y')


class Parking_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ('id', 'parking_name', 'parking_Street', 'parking_City', 'x','y','free_places')
        read_only_fields = ('id','x','y')


class User_Serializer(serializers.ModelSerializer):
        class Meta:
            model = CustomUser
            fields = ('email')
            # extra_kwargs = {'password': {'write_only': True}}

            # def create(self, validated_data):   ###Walidacja hasla
            #     user = User_Client(
            #         email=validated_data['email'],
            #         login=validated_data['login']
            #     )
            #     user.set_password(validated_data['password'])
            #     user.save()
            #     return user
            #

class User_Serializer_Login_Email(serializers.ModelSerializer):
        class Meta:
            model = CustomUser
            fields = ('email')


class Booking_Serializer(serializers.ModelSerializer):
        class Meta:
                model = Booking
                fields = ('code', 'parking', 'Date_From', 'Date_To', 'Cost', 'user','registration_plate')
                read_only_fields = ('parking', 'Date_From', 'Date_To','user','registration_plate')


