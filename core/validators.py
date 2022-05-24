from dadata import Dadata
from django.conf import settings
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
            raise ValidationError(f"{value} должен лежать в диапазоне от {self.min_value} до {self.max_value}")

    def __eq__(self, other):
        return self.min_value == other.min_value and self.max_value == other.max_value


@deconstructible
class AddressValidator(object):
    def __init__(self, query: str, city: str, fias: str):
        self.query = query
        self.city = city
        self.fias = fias

    def __call__(self):
        with Dadata(settings.DADATA_API_KEY, settings.DADATA_SECRET_KEY) as dadata:
            response = dadata.find_by_id(name="address", query=self.fias)

            if not response:
                raise ValidationError(f"ФИАС идентификатор {self.fias} не существует")
            if response[0]["value"] != self.query:
                raise ValidationError(f"ФИАС идентификатор не соответствует адресу")
            if response[0]["data"]["city"] != self.city:
                raise ValidationError(f"Город, соответсвующий идентификатору ФИАС не соответствует введенному")

    def __eq__(self, other):
        return self.query == other.query and self.city == other.city and self.fias == other.fias
