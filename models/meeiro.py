from typing import Optional, List

from sqlalchemy import exc
from sqlalchemy.orm import Session

from models.exceptions import DuplicatedValue, RowNotFound
from orm.planting import Meeiro as MeeiroMapping


class Meeiro:
    def __init__(self, id_: int, name: str, cpf: str, rg: str, db_connection: Session):
        self._rg = rg
        self._cpf = cpf
        self._name = name
        self._id = id_
        self._db_connection = db_connection

    @property
    def rg(self):
        return self._rg

    @property
    def cpf(self):
        return self._cpf

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @classmethod
    def get_meeiro(cls, db_connection: Session, id_: int = None, cpf: str = None) -> Optional['Meeiro']:
        """
        Obtém o objeto meeiro do banco de dados a partir do filtro enviado, id e ou cpf.
        Caso não exista ou nenhum filtro seja enviado, retorna None.
        :param db_connection: sessão de conexão com o banco de dados.
        :param id_: filtro para o id do meeiro
        :param cpf: filtro para o cpf do meeiro
        :return: este objeto
        """

        if any([id_, cpf]):
            filter_ = []
            if id_:
                filter_.append(MeeiroMapping.id == id_)
            if cpf:
                filter_.append(MeeiroMapping.cpf == cpf)

            meeiro = db_connection.query(MeeiroMapping).filter(*filter_).first()

            if not meeiro:
                raise RowNotFound('Meeiro não encontrado para os filtros: id {} cpf {}'.format(
                    id_, cpf
                ))

            return Meeiro(meeiro.id, meeiro.name, meeiro.cpf, meeiro.rg, db_connection)
        raise ValueError('Parametros inválidos para obter meeiro.')

    @classmethod
    def list(cls, db_connection: Session) -> List['Meeiro']:
        """
        Obtém todos os meeiros que existem cadastrados no banco.
        :param db_connection: sessão de conexão com o banco de dados.
        :return: lista de objetos
        """

        meeiros = db_connection.query(MeeiroMapping).all()

        list_meeiros = [Meeiro(m.id, m.name, m.cpf, m.rg, db_connection) for m in meeiros]

        return list_meeiros

    @classmethod
    def insert(cls, db_connection: Session, cpf: str, rg: str, name: str):
        """
        Insere um novo meeiro no banco de dados e retorna o objeto.
        Não trata erros de banco.
        :param db_connection: sessão do banco de dados
        :param cpf: cpf do meeiro
        :param rg: rg do meeiro
        :param name: nome do meeiro
        :return: este objeto
        """
        new_obj = MeeiroMapping()
        new_obj.cpf = cpf
        new_obj.rg = rg
        new_obj.name = name
        try:
            db_connection.add(new_obj)
            db_connection.flush()
            db_connection.commit()
        except exc.IntegrityError:
            db_connection.rollback()
            raise DuplicatedValue("Este meeiro já está cadastrado. Para alterar seus dados,"
                                  "use a opção Alterar Meeiro.")

        return True

    @classmethod
    def update(cls, db_connection: Session, new_cpf: str, new_rg: str, new_name: str, id_: int) -> bool:

        try:
            current_cpf = cls.get_meeiro(db_connection, cpf=new_cpf)
            if current_cpf and current_cpf.id != id_:
                raise DuplicatedValue("Este CPF já está sendo usado para o meeiro: {}".format(current_cpf.name))
        except RowNotFound:
            pass

        result_set = db_connection.query(MeeiroMapping).filter(MeeiroMapping.id == id_).update(
            {MeeiroMapping.rg: new_rg, MeeiroMapping.name: new_name, MeeiroMapping.cpf: new_cpf}
        )
        db_connection.commit()
        if result_set:
            return True

        db_connection.rollback()
        return False

