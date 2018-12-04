from datetime import datetime

from views.dtos.entry_type import EntryTypeDto
from views.dtos.meeiro import MeeiroDto


class EntryDto:
    def __init__(self, id_: int, meeiro: MeeiroDto, entry_date: datetime, entry_type: EntryTypeDto,
                 entry_value: float, description: str):
        self.id_ = id_
        self.meeiro = meeiro
        self.entry_date = entry_date
        self.entry_type = entry_type
        self.entry_value = entry_value
        self.description = description
