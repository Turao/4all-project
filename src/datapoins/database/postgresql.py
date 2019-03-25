from playhouse.pool import PooledPostgresqlExtDatabase
import os


class PostgreSQLProvider():
    def __init__(self, logger=None):
        self.database = PooledPostgresqlExtDatabase(
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT'),
            max_connections=os.environ.get('DB_POOL_MAX_CONNECTIONS'),
            stale_timeout=os.environ.get('DB_POOL_TIMEOUT'),
        )
        self.open_connection()
        self.logger = logger

    def __del__(self):
        self.close_connection()

    def open_connection(self):
        self.database.connect(reuse_if_open=True)
        print('Connected to PostgreSQL database')

    def close_connection(self):
        self.database.close()
        print('Connection to PostgreSQL database closed')


if __name__ == '__main__':
    PostgreSQLProvider()
