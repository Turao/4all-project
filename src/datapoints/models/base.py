from peewee import (
    chunked,
    Model,
    PeeweeException,
)
from ..database.postgresql import PostgreSQLProvider


class BaseModel(Model):
    class Meta:
        conn = PostgreSQLProvider()
        database = conn.database

    @classmethod
    def bulk_create_safe(cls, data, batch_size=100):
        with cls._meta.database.atomic() as transaction:
            try:
                cls.bulk_create(data, batch_size)
            except PeeweeException as pwex:
                transaction.rollback()
                print(pwex)

    @classmethod
    def insert_many_safe(cls, models, batch_size=100):
        with cls._meta.database.atomic() as transaction:
            try:
                for batch in chunked(models, 100):
                    cls.insert_many(models)
            except PeeweeException as pwex:
                transaction.rollback()
                print(pwex)
