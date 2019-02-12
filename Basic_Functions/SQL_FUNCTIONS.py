from django.db.models import Sum


def sum_field_from_query(query,field_name):

    if not query.exists():
        return 0

    else:
        field__sum=field_name+'__sum'
        sum = query.aggregate(Sum(field_name))[field__sum]
        return sum
