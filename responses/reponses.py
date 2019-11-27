from rest_framework import status
from rest_framework.response import Response


def user_inactive():
    content = {'Requested user': 'inactive, confirm you email in order to log in'}
    return Response(content, status=status.HTTP_401_UNAUTHORIZED)

def user_not_in_group():
    content = {'Requested user': 'not in group, cannot login'}
    return Response(content, status=status.HTTP_401_UNAUTHORIZED)


def user_created():
    content = {'Requested user': 'not in group, cannot login'}
    return Response(content, status=status.HTTP_201_CREATED)


def empty_view(self):
    content = {'please move along': 'nothing to see here'}
    return Response(content, status=status.HTTP_404_NOT_FOUND)


class BaseCustomException(Exception):
    status_code = None
    error_message = None
    is_an_error_response = True
    def __init__(self, error_message):
        Exception.__init__(self)
        self.error_message = error_message
    def to_dict(self):
        return {'errorMessage': self.error_message}


class UNAUTHORIZED(BaseCustomException):
    status_code = 401

class FORBIDDEN(BaseCustomException):
    status_code = 403
