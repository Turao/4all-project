from peewee import Model
from ..database.postgresql import PostgreSQLProvider


class BaseModel(Model):
    class Meta:
        conn = PostgreSQLProvider()
        database = conn.database