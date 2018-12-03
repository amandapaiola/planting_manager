from sqlalchemy.orm import Session

from orm.planting import EntryType as EntryTypeMapping
from models.exceptions import RowNotFound


class EntryType:
    def __init__(self, id_: int, name: str, db_connection: Session):
        self.id = id_
        self.name = name
        self.db_connection = db_connection

    @classmethod
    def get_entry_type(cls, id_: int, db_connection: Session):
        """
        Obtém o objeto correspondente ao tipo de lançamento do id passado.
        :raises: RowNotFound
        :param id_: id do lançamento
        :param db_connection: conexão com banco de dados
        :return: objeto EntryType
        """
        entry_type = db_connection.query(EntryTypeMapping).filter(EntryTypeMapping.id == id_).first()
        if not entry_type:
            raise RowNotFound('Este tipo de lançamento não foi encontrado. Id: {}'.format(id_))
        return EntryType(id_=entry_type.id, name=entry_type.name, db_connection=db_connection)
