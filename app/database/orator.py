import logging
import os

databases = {
    'postgres': {
        'driver': 'postgres',
        'host': os.getenv('DB_HOST'),
        'port': int(os.getenv('DB_PORT')),
        'database': os.getenv('DB_DATABASE'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'prefix': '',
        'log_queries': True,
    },
}


logger = logging.getLogger('orator.connection.queries')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    'It took %(elapsed_time)sms to execute the query %(query)s'
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)
