from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

# django database data (model) validators


## validate serial codes for students
def serial_code_validator(value):
    if len(value) != 6:
        message = _('کد سریال باید ۶ رقمی باشد')
        raise ValidationError(message)
    try:
        int(value)
    except ValueError:
        message = _('فقط اعداد قابل قبول است')
        raise ValidationError(message)


## validate identifiers for students
def student_id_validator(value):
    if len(value) != 10:
        message = _('کد ملی باید ۱۰ رقمی باشد')
        raise ValidationError(message)
    try:
        int(value)
    except ValueError:
        message = _('فقط اعداد قابل قبول است')
        raise ValidationError(message)