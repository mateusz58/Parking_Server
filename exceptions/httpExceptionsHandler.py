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
class STATUS_CHANGE(BaseCustomException):
    status_code = 200
