from orator import DatabaseManager
from orator import Model

from .orator import databases

DATABASES = databases
DB = DatabaseManager(databases)
Model.set_connection_resolver(DB)
