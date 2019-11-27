from django.core.validators import RegexValidator

isalphavalidator = RegexValidator(r'^[\w]*$',
                             message='name must be alphanumeric',
                             code='Invalid name')
