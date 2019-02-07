


from rest_framework import serializers
from bikes.models import Bike
from rest_framework import serializers
from bikes.models import Bike

class BikeSerializer(serializers.ModelSerializer):
    COLOR_OPTIONS = ('yellow', 'black')

    color = serializers.ChoiceField(choices=COLOR_OPTIONS)
    size = serializers.FloatField(min_value=30.0, max_value=60.0)

    class Meta:
        model = Bike
        fields = ['color', 'size']




class BikeSerializer(serializers.ModelSerializer):
    COLOR_OPTIONS = ('yellow', 'black')

    color = serializers.ChoiceField(choices=COLOR_OPTIONS)
    size = serializers.FloatField(min_value=30.0, max_value=60.0)

    class Meta:
        model = Bike
        fields = ['color', 'size']


def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(['color', 'size']))


def test_color_field_content(self):
        data = self.serializer.data

        self.assertEqual(data['color'], self.bike_attributes['color'])


def test_size_field_content(self):
        data = self.serializer.data

        self.assertEqual(data['size'], float(self.bike_attributes['size']))


def test_size_lower_bound(self):
        self.serializer_data['size'] = 29.9

        serializer = BikeSerializer(data=self.serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['size']))


def test_size_upper_bound(self):
        self.serializer_data['size'] = 60.1

        serializer = BikeSerializer(data=self.serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['size']))


def test_float_data_correctly_saves_as_decimal(self):
        self.serializer_data['size'] = 31.789

        serializer = BikeSerializer(data=self.serializer_data)
        serializer.is_valid()

        new_bike = serializer.save()
        new_bike.refresh_from_db()

        self.assertEqual(new_bike.size, Decimal('31.79'))

def test_color_must_be_in_choices(self):
        self.bike_attributes['color'] = 'red'

        serializer = BikeSerializer(instance=self.bike, data=self.bike_attributes)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['color']))