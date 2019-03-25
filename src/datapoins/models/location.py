from peewee import (
    CharField,
    Check,
    DateTimeField,
    DoubleField,
    IntegerField,
)
from datetime import datetime
from .base import BaseModel


class Location(BaseModel):
    latitude = DoubleField(constraints=[
        Check('-90 < latitude AND latitude < 90')
    ])
    longitude = DoubleField(constraints=[
        Check('-180 < longitude AND longitude < 180')
    ])

    _type = CharField(null=True)
    country = CharField(null=True)
    country_code = CharField(null=True)
    state = CharField(null=True)
    city = CharField(null=True)
    district = CharField(null=True)
    postcode = CharField(null=True)
    street = CharField(null=True)
    number = IntegerField(null=True)

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.__class__}: {self.__data__}'


Location().create_table(safe=True)
