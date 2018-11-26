from typing import List

from sqlalchemy.orm import Session

from models.exceptions import DuplicatedValue
from models.meeiro import Meeiro
from views.dtos.meeiros import MeeiroDto


class MeeiroController:
    def __init__(self, db_connection: Session):
        self.db_connection = db_connection

    def insert_new_meeiro(self, name: str, cpf: str, rg: str) -> (bool, str):
        try:
            Meeiro.insert(self.db_connection, cpf, rg, name)
            return True, 'Inserido com Sucesso!'
        except DuplicatedValue as error:
            return False, error

    def list(self) -> List[MeeiroDto]:
        meeiros = Meeiro.get_meeiros(self.db_connection)
        serialized_list = []
        for m in meeiros:
            serialized_list.append(MeeiroDto(name=m.name,
                                             cpf=m.cpf,
                                             rg=m.rg,
                                             id_=m.id_))
        return serialized_list

    def update(self, id_: int, cpf: str, rg: str, name: str):
        try:
            updated = Meeiro.update_meeiro(self.db_connection, new_cpf=cpf, new_rg=rg, new_name=name, id_=id_)
            if updated:
                return True, 'Alterado com sucesso!'
            else:
                return False, 'Erro inesperado. Tente novamente.'
        except DuplicatedValue as error:
            return False, error
