import re

from django.db.models import Sum


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def check_query_string(value):
    if not hasNumbers(str(value)): return 0
    else:
            value = (value.all().aggregate(Sum('number_of_cars')))
            value = re.sub("\D", "", str(value))
            value = int(value)
            return value