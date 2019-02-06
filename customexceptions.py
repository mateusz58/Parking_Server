# HTTP_200_OK
# HTTP_201_CREATED
# HTTP_202_ACCEPTED
# HTTP_203_NON_AUTHORITATIVE_INFORMATION
# HTTP_204_NO_CONTENT
# HTTP_205_RESET_CONTENT
# HTTP_206_PARTIAL_CONTENT
# HTTP_207_MULTI_STATUS
# HTTP_400_BAD_REQUEST
# HTTP_401_UNAUTHORIZED
# HTTP_402_PAYMENT_REQUIRED
# HTTP_403_FORBIDDEN
# HTTP_404_NOT_FOUND
# HTTP_405_METHOD_NOT_ALLOWED
# HTTP_406_NOT_ACCEPTABLE
# HTTP_407_PROXY_AUTHENTICATION_REQUIRED
# HTTP_408_REQUEST_TIMEOUT
# HTTP_409_CONFLICT
# HTTP_410_GONE
# HTTP_411_LENGTH_REQUIRED
# HTTP_412_PRECONDITION_FAILED
# HTTP_413_REQUEST_ENTITY_TOO_LARGE
# HTTP_414_REQUEST_URI_TOO_LONG
# HTTP_415_UNSUPPORTED_MEDIA_TYPE
# HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
# HTTP_417_EXPECTATION_FAILED
# HTTP_422_UNPROCESSABLE_ENTITY
# HTTP_423_LOCKED
# HTTP_424_FAILED_DEPENDENCY
# HTTP_428_PRECONDITION_REQUIRED
# HTTP_429_TOO_MANY_REQUESTS
# HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE
# HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS







class BaseCustomException(Exception):
    status_code = None
    error_message = None
    is_an_error_response = True
    def __init__(self, error_message):
        Exception.__init__(self)
        self.error_message = error_message
    def to_dict(self):
        return {'errorMessage': self.error_message}

class InvalidUsage(BaseCustomException):
    status_code = 400
class UNAUTHORIZED(BaseCustomException):
    status_code = 401
class FORBIDDEN(BaseCustomException):
    status_code = 403

# ## HOW To USE
# from django.http import JsonResponse
# from customexceptions import InvalidUsage
# def do_something():
#     if bad_data:
#         raise InvalidUsage("Bad Request! Data is poorly formatted")
# def a_view(request):
#     do_something()
#     return JsonResponse({'message': "no errors!'}, 200)