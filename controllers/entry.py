from typing import List

from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from sqlalchemy.orm import Session

from controllers.entry_type import EntryTypeController
from controllers.meeiro import MeeiroController
from models.entry import Entry
from models.exceptions import RowNotFound
from models.filter_helper import DateRange
from views.dtos.entry import EntryDto


class EntryController:
    def __init__(self, db_connection: Session):
        self.db_connection = db_connection
        self.meeiro_controller = MeeiroController(self.db_connection)
        self.entry_type_controller = EntryTypeController(self.db_connection)

    def insert_new_entry(self, meeiro_id: int, entry_date: datetime, entry_type_id: int, entry_value: float,
                         description: str) -> (bool, str):
        try:
            Entry.insert(meeiro_id=meeiro_id, entry_date=entry_date, entry_type_id=entry_type_id,
                         entry_value=entry_value, description=description, db_session=self.db_connection)
            return True, 'Inserido com Sucesso!'
        except (SQLAlchemyError, RowNotFound) as error:
            # TODO logar o erro
            return False, 'Erro ao inserir.'

    def list(self, meeiro_id: int, entry_type: int = None, max_date: datetime = None,
             min_date: datetime = None) -> List[EntryDto]:
        date_range = None
        if max_date and min_date:
            date_range = DateRange(max_date=max_date, min_date=min_date, use_equal=True)
        filters = Entry.get_filters_to_query_entry(self.db_connection, meeiro_id=meeiro_id,
                                                   entry_type_id=entry_type, date_filter=date_range)
        entries = Entry.get_entries(self.db_connection, filters)
        serialized_list = []
        for e in entries:
            meeiro = self.meeiro_controller.get_meeiro(id_=e.meeiro_id)
            entry_type = self.entry_type_controller.get(e.entry_type_id)
            serialized_list.append(EntryDto(id_=e.id_, meeiro=meeiro, entry_date=e.entry_date,
                                            entry_type=entry_type, entry_value=e.entry_value,
                                            description=e.description))
        return serialized_list

