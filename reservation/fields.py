from django.core.exceptions import ValidationError
from django.db.models import FloatField


def validate_number(number: float):
    if number < 0 or number > 1:
        raise ValidationError("Value should not be greater than 1 or lesser than 0!")


class PercentageField(FloatField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(validate_number)
