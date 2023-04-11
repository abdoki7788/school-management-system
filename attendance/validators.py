from django.core.exceptions import ValidationError

def serial_code_validator(value):
    if len(value) != 6:
        message = 'serial code length should be 6.'
        raise ValidationError(message)
    try:
        int(value)
    except ValueError:
        message = 'it should be a valid number'
        raise ValidationError(message)


def student_id_validator(value):
    if len(value) != 10:
        message = 'id length should be 10.'
        raise ValidationError(message)
    try:
        int(value)
    except ValueError:
        message = 'it should be a valid number'
        raise ValidationError(message)