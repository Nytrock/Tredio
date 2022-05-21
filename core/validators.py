from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class RangeValidator(object):
    def __init__(self, min_value=1, max_value=5):
        assert min_value < max_value
        self.min_value, self.max_value = min_value, max_value
        self.validators = [MinValueValidator(min_value), MaxValueValidator(max_value)]

    def __call__(self, value):
        try:
            [validator(value) for validator in self.validators]
        except ValidationError:
            raise ValidationError(f"{value} должен лежать в диапазоне от {min_value} до {max_value}")

    def __eq__(self, other):
        return self.min_value == other.min_value and self.max_value == other.max_value
