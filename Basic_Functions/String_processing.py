import re

from django.db.models import Sum


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def check_query_string(value):
    if not hasNumbers(str(value)): return 0
    else:
            value = (value.all().aggregate(Sum('booking__number_of_cars')))
            value = re.sub("\D", "", str(value))
            value = int(value)
            return value


def is_all_items_unique(input_list):
    first_element = input_list[0]
    for element in input_list:
        if element != first_element:
            return False

    return True