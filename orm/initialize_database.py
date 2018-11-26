from orm.postgres_connection import Connection
from orm.planting import Base

connection = Connection('postgres', 'root', '127.0.0.1:5432', 'auto_teste')

Base.metadata.create_all(connection.engine)