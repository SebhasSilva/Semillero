# users/validators.py

import re
from django.core.exceptions import ValidationError

def validate_registration_id(value):
    if not re.match(r'^[1-9]{6}$', value):
        raise ValidationError('El ID de registro debe tener 6 números del 1 al 9.')