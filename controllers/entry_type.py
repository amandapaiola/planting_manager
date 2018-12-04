from sqlalchemy.orm import Session

from models.entry_type import EntryType
from views.dtos.entry_type import EntryTypeDto


class EntryTypeController:
    def __init__(self, db_connection: Session):
        self.db_connection = db_connection

    def list(self):
        return EntryType.list(self.db_connection)

    def get(self, id_: int) -> EntryTypeDto:
        entry_type = EntryType.get_entry_type(id_=id_, db_connection=self.db_connection)
        return EntryTypeDto(name=entry_type.name, id_=entry_type.id)
