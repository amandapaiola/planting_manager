from sqlalchemy import exc

from orm.planting import Base, Meeiro
from orm.postgres_connection import Connection


def initialize_database():
    root = Connection('postgres', 'root', '127.0.0.1:5432', 'postgres')
    root_session = root.session()
    root_session.connection().connection.set_isolation_level(0)
    try:
        print("Trying to create database...")
        root_session.execute("CREATE DATABASE planting_manager_teste")
        root_session.connection().connection.set_isolation_level(1)
    except exc.ProgrammingError:
        print("Trying to remove already exists database and creating...")
        root_session.execute("DROP DATABASE planting_manager_teste")
        root_session.execute("CREATE DATABASE planting_manager_teste")

    root_session.close_all()

    connection = Connection('postgres', 'root', '127.0.0.1:5432', 'planting_manager_teste')
    Base.metadata.create_all(connection.engine)
    print("Initialized database")


def clear_database():
    connection = Connection('postgres', 'root', '127.0.0.1:5432', 'planting_manager_teste')
    session = connection.session()
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
        print('Deleted table {}'.format(table.name))
    session.commit()
    session.close_all()
    print("Cleared all database")


def destroy_database():
    root = Connection('postgres', 'root', '127.0.0.1:5432', 'postgres')
    root_session = root.session()
    root_session.connection().connection.set_isolation_level(0)
    root_session.execute("""SELECT pg_terminate_backend(pid) 
                            FROM pg_stat_activity WHERE datname = 'planting_manager_teste';""")
    root_session.execute("DROP DATABASE planting_manager_teste")
    root_session.connection().connection.set_isolation_level(1)
    root_session.close_all()
    print("Dropped database...")


def create_meeiro(name: str, cpf: str, rg: str) -> int:
    connection = Connection('postgres', 'root', '127.0.0.1:5432', 'planting_manager_teste')
    session = connection.session()
    meeiro_obj = Meeiro()
    meeiro_obj.name = name
    meeiro_obj.cpf = cpf
    meeiro_obj.rg = rg
    session.add(meeiro_obj)
    session.flush()
    session.commit()
    meeiro_id = meeiro_obj.id
    session.close()

    return meeiro_id
