from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from models.entry_type import EntryType
from models.filter_helper import DataRange, NumValueLimit
from models.meeiro import Meeiro
from orm.planting import Entry as EntryMapping


class Entry:
    def __init__(self, id_: int, meeiro_id: int, entry_date: datetime, entry_type_id: int, entry_value: float,
                 description: str, db_connection: Session):
        self.id_ = id_
        self.meeiro_id = meeiro_id
        self.entry_date = entry_date
        self.entry_type_id = entry_type_id
        self.entry_value = entry_value
        self.description = description
        self.db_connection = db_connection

    @classmethod
    def insert(cls, meeiro_id: int, entry_date: datetime, entry_type_id: int, entry_value: float,
               description: str, db_session: Session):
        """
        :raises RowNotFound: caso de valores inválidos como meeiro e tipo de lançamento

        :param meeiro_id:
        :param entry_date:
        :param entry_type_id:
        :param entry_value:
        :param description:
        :param db_session:
        :return:
        """

        meeiro = Meeiro.get_meeiro(db_connection=db_session, id_=meeiro_id)
        entry_type = EntryType.get_entry_type(entry_type_id, db_connection=db_session)

        entry = EntryMapping()
        entry.meeiro_id = meeiro.id
        entry.entry_date = entry_date
        entry.entry_type = entry_type.id
        entry.entry_value = entry_value
        entry.description = description

        db_session.add(entry)
        db_session.commit()


    @staticmethod
    def get_filters_to_query_entry(db_session: Session, meeiro_id: int = None, date_filter: DataRange = None,
                                   entry_type_id: int = None, filter_value: NumValueLimit = None) -> List:
        filters = []
        if meeiro_id:
            meeiro = Meeiro.get_meeiro(db_connection=db_session, id_=meeiro_id)
            filters.append(EntryMapping.meeiro_id == meeiro.id)
        if entry_type_id:
            entry_type = EntryType.get_entry_type(entry_type_id, db_connection=db_session)
            filters.append(EntryMapping.entry_type == entry_type.id)

        if date_filter:
            filters.append(date_filter.get_filter(EntryMapping.entry_date))

        if filter_value:
            filters.append(filter_value.get_filter(EntryMapping.entry_value))

        return filters

    @classmethod
    def get_entries(cls, db_session: Session, filters: List) -> List['Entry']:
        """
        Obtém os lançamentos de acordo com os filtros passados.
        Para obter os filtros utilize o método get_filters_to_query_entry desta classe.
        :param db_session:
        :param filters:
        :return:
        """
        result_set = db_session.query(EntryMapping).filter(*filters).all()
        entries = []
        for e in result_set:
            entries.append(Entry(id_=e.id, meeiro_id=e.meeiro_id, entry_date=e.entry_date,
                                 entry_type_id=e.entry_type, entry_value=e.entry_value,
                                 description=e.description, db_connection=db_session))
        return entries
