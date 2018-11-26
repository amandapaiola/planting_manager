from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, func, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Meeiro(Base):
    __tablename__ = 'meeiro'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    rg = Column(String, nullable=False)
    created_at = Column(DateTime(True), server_default=func.current_timestamp())
    modified_at = Column(DateTime(True), server_default=func.current_timestamp(), server_onupdate=func.current_timestamp())

    UniqueConstraint('id', 'cpf', name='meeiro_unique_constraint')

    def __repr__(self):
        return "<User(name='%s', cpf='%s', rg='%s')>" % (self.name, self.cpf, self.rg)


class BoxType(Base):
    __tablename__ = 'box_type'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class EntryType(Base):
    __tablename__ = 'entry_type'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Harvest(Base):
    """
        Colheita
    """

    __tablename__ = 'harvest'

    id = Column(Integer, primary_key=True)
    meeiro_id = Column(Integer, nullable=False)
    harvest_date = Column(DateTime(timezone=True), nullable=False)
    box_type = Column(Integer, ForeignKey("box_type.id"), nullable=False)
    box_value = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(True), server_default=func.current_timestamp())
    modified_at = Column(DateTime(True), server_default=func.current_timestamp(), onupdate=func.current_timestamp())


class Entry(Base):
    """
        Lançamentos
    """

    __tablename__ = 'entry'

    id = Column(Integer, primary_key=True)
    meeiro_id = Column(Integer, nullable=False)
    entry_date = Column(DateTime(timezone=True), nullable=False)
    entry_type = Column(Integer, ForeignKey("entry_type.id"), nullable=False)
    entry_value = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime(True), server_default=func.current_timestamp())
    modified_at = Column(DateTime(True), server_default=func.current_timestamp(), onupdate=func.current_timestamp())
