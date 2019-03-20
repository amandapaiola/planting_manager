from sqlalchemy.orm import Session

from orm.planting import EntryType as EntryTypeMapping, EntryType
from models.exceptions import RowNotFound


class EntryTypeModel:
    def __init__(self, id_: int, name: str, db_connection: Session):
        self.id = id_
        self.name = name
        self.db_connection = db_connection

    @classmethod
    def get_entry_type(cls, db_connection: Session, id_: int):
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
        return EntryTypeModel(id_=entry_type.id, name=entry_type.name, db_connection=db_connection)

    @classmethod
    def list(cls, session: Session):
        result_set = session.query(EntryTypeMapping).all()
        entry_types = []
        for result in result_set:
            entry_types.append(EntryTypeModel(result.id, result.name, session))
        return entry_types

    @classmethod
    def insert(cls, db_connection: Session, name: str):
        """
        Insere um novo tipo de lançamento.
        :param db_connection: conexão com o banco de dados.
        :param name: nome da nova entry.
        :return:
        """

        entry_type = EntryType()
        entry_type.name = name.lower()

        try:
            db_connection.add(entry_type)
            db_connection.flush()
            db_connection.commit()
        except exc.IntegrityError:
            db_connection.rollback()
            raise DuplicatedValue("Este tipo já está cadastrado.")
