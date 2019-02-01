from django.core.exceptions import ValidationError

class validate_range_min_max(object):
    compare = lambda self, a, b, c: a > c or a < b
    clean = lambda self, x: x
    message = ('Ensure this value is between %(limit_min)s and %(limit_max)s (it is %(show_value)s).')
    code = 'limit_value'

    def __init__(self, limit_min, limit_max):
        self.limit_min = limit_min
        self.limit_max = limit_max

    def __call__(self, value):
        cleaned = self.clean(value)
        params = {'limit_min': self.limit_min, 'limit_max': self.limit_max, 'show_value': cleaned}
        if value:  # make it optional, remove it to make required, or make required on the model
            if self.compare(cleaned, self.limit_min, self.limit_max):
                raise ValidationError(self.message, code=self.code, params=params)



