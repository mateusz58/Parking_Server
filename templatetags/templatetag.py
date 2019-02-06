from django import template
from django.contrib.auth.models import Group

from users.models import CustomUser

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='has_group_v2')
def has_group_v2(user, group_name):
    return CustomUser.objects.get(email=user).groups.filter(name=group_name).exists()


@register.filter
def is_false(arg):
    return arg is False


@register.filter(name='is_active')
def is_user_active(user):
    return CustomUser.objects.get(email=user).is_active

