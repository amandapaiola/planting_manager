from datetime import datetime

from enum import Enum

from sqlalchemy.sql.elements import and_


class DataRange:
    def __init__(self, max_date: datetime, min_date: datetime, use_equal: bool=True):
        self.max_date = max_date
        self.min_date = min_date
        self.use_equal = use_equal

    def get_filter(self, column):
        """
        Obtém o filtro de acordo com o range de datas passados na coluna column.
        :param column: coluna para filtrar. Essa coluna deve ser do tipo datetime.
        :return: filtro do sqlalchemy
        """
        if self.use_equal:
            filter_ = and_(column >= self.min_date, column <= self.max_date)
        else:
            filter_ = and_(column > self.min_date, column < self.max_date)

        return filter_


class Operation(Enum):
    GREATER_THAN = 1
    LESS_THAN = 2


class NumValueLimit:
    def __init__(self, value: float, operation: Operation, use_equal: bool=True):
        self.value = value
        self.operation = operation
        self.use_equal = use_equal

    def get_filter(self, column):
        """
        Obtém o filtro de acordo com o limite passado para construção do filtro na coluna.
        :param column: coluna para filtrar. Essa coluna deve conter valor númerico.
        :return: filtro do sqlalchemy
        """
        if self.use_equal:
            if self.operation.value == Operation.GREATER_THAN.value:
                filter_ = column >= self.value
            elif self.operation.value == Operation.LESS_THAN.value:
                filter_ = column <= self.value
            else:
                raise ValueError("Operação para filtro inválida.")
        else:
            if self.operation.value == Operation.GREATER_THAN.value:
                filter_ = column > self.value
            elif self.operation.value == Operation.LESS_THAN.value:
                filter_ = column < self.value
            else:
                raise ValueError("Operação para filtro inválida.")

        return filter_
