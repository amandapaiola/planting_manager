from unittest import TestCase
import pytz

from datetime import datetime

from models.entry import Entry
from models.filter_helper import DateRange, NumValueLimit, Operation
from models.exceptions import RowNotFound
from orm.planting import Entry as EntryMapping
from orm.postgres_connection import Connection
from tests.test_helper.test_helper import create_meeiro, initialize_database, clear_database, destroy_database, \
    create_entry_type


class EntryModelTest(TestCase):

    @classmethod
    def tearDownClass(cls):
        destroy_database()

    @classmethod
    def setUpClass(cls):
        initialize_database()

    def tearDown(self):
        clear_database()

    def test_insert_entry__expect_correct_insert(self):
        connection = Connection('postgres', 'root', '127.0.0.1:5432', 'planting_manager_teste')
        session = connection.session()
        meeiro_id = create_meeiro(name='tadeu', cpf='55584447213', rg='50658045x')
        entry_type_id = create_entry_type('despesas', connection)
        session.expunge_all()
        session.close()

        Entry.insert(meeiro_id=meeiro_id, entry_date=datetime(2018, 10, 1),
                     entry_type_id=entry_type_id, entry_value=100.0,
                     description='veneno', db_session=connection.session())

        america_timezone = pytz.timezone('America/Sao_Paulo')
        entry = session.query(EntryMapping).one()
        self.assertEqual(entry.entry_type, entry_type_id)
        self.assertEqual(str(entry.entry_date), str(america_timezone.localize(datetime(2018, 10, 1))))
        self.assertEqual(entry.meeiro_id, meeiro_id)
        self.assertEqual(entry.description, 'veneno')
        self.assertEqual(entry.entry_value, 100.0)

    def test_insert_entry__invalid_meeiro__expect_raise_error(self):
        connection = Connection('postgres', 'root', '127.0.0.1:5432', 'planting_manager_teste')
        session = connection.session()
        entry_type_id = create_entry_type('despesas', connection)
        session.expunge_all()
        session.close()

        with self.assertRaises(RowNotFound):
            Entry.insert(meeiro_id=21, entry_date=datetime(2018, 10, 1),
                         entry_type_id=entry_type_id, entry_value=100.0,
                         description='veneno', db_session=connection.session())

    def test_insert_entry__invalid_entry_type__expect_raise_error(self):
        connection = Connection('postgres', 'root', '127.0.0.1:5432', 'planting_manager_teste')
        session = connection.session()
        meeiro_id = create_meeiro(name='tadeu', cpf='55584447213', rg='50658045x')
        session.expunge_all()
        session.close()

        with self.assertRaises(RowNotFound):
            Entry.insert(meeiro_id=meeiro_id, entry_date=datetime(2018, 10, 1),
                         entry_type_id=23, entry_value=100.0,
                         description='veneno', db_session=connection.session())

    def test_get_entries__filter_by_meeiro_id__expected_correct_result(self):
        connection = Connection('postgres', 'root', '127.0.0.1:5432', 'planting_manager_teste')
        session = connection.session()
        meeiro_id = create_meeiro(name='tadeu', cpf='55584447213', rg='50658045x')
        entry_type_id = create_entry_type('despesas', connection)
        session.expunge_all()
        session.close()

        execute_session = connection.session()
        Entry.insert(meeiro_id=meeiro_id, entry_date=datetime(2018, 10, 1),
                     entry_type_id=entry_type_id, entry_value=100.0,
                     description='veneno', db_session=execute_session)

        filters_ = Entry.get_filters_to_query_entry(db_session=execute_session, meeiro_id=meeiro_id)
        entries = Entry.get_entries(execute_session, filters_)
        self.assertEqual(len(entries), 1)
        expected_entry = entries[0]

        america_timezone = pytz.timezone('America/Sao_Paulo')
        self.assertEqual(expected_entry.entry_type_id, entry_type_id)
        self.assertEqual(str(expected_entry.entry_date), str(america_timezone.localize(datetime(2018, 10, 1))))
        self.assertEqual(expected_entry.meeiro_id, meeiro_id)
        self.assertEqual(expected_entry.description, 'veneno')
        self.assertEqual(expected_entry.entry_value, 100.0)

    def test_get_entries__filter_by_range_date__expected_correct_result(self):
        america_timezone = pytz.timezone('America/Sao_Paulo')

        connection = Connection('postgres', 'root', '127.0.0.1:5432', 'planting_manager_teste')
        session = connection.session()
        meeiro_id = create_meeiro(name='tadeu', cpf='55584447213', rg='50658045x')
        entry_type_id = create_entry_type('despesas', connection)
        session.expunge_all()
        session.close()

        execute_session = connection.session()
        Entry.insert(meeiro_id=meeiro_id, entry_date=america_timezone.localize(datetime(2018, 10, 2, 1, 1)),
                     entry_type_id=entry_type_id, entry_value=100.0,
                     description='veneno', db_session=execute_session)

        Entry.insert(meeiro_id=meeiro_id, entry_date=america_timezone.localize(datetime(2018, 10, 1, 23, 58)),
                     entry_type_id=entry_type_id, entry_value=1520.0,
                     description='combustivel', db_session=execute_session)

        filters_ = Entry.get_filters_to_query_entry(db_session=execute_session,
                                                    date_filter=
                                                    DateRange(min_date=america_timezone.localize(datetime(2018, 10, 1, 23, 59)),
                                                              max_date=america_timezone.localize(datetime(2018, 10, 2, 1, 10)),
                                                              use_equal=True),
                                                    )
        entries = Entry.get_entries(execute_session, filters_)
        self.assertEqual(len(entries), 1)
        expected_entry = entries[0]

        self.assertEqual(expected_entry.entry_type_id, entry_type_id)
        self.assertEqual(str(expected_entry.entry_date), str(america_timezone.localize(datetime(2018, 10, 2, 1, 1))))
        self.assertEqual(expected_entry.meeiro_id, meeiro_id)
        self.assertEqual(expected_entry.description, 'veneno')
        self.assertEqual(expected_entry.entry_value, 100.0)

    def test_get_entries__filter_by_value__expected_correct_result(self):
        america_timezone = pytz.timezone('America/Sao_Paulo')

        connection = Connection('postgres', 'root', '127.0.0.1:5432', 'planting_manager_teste')
        session = connection.session()
        meeiro_id = create_meeiro(name='tadeu', cpf='55584447213', rg='50658045x')
        entry_type_id = create_entry_type('despesas', connection)
        session.expunge_all()
        session.close()

        execute_session = connection.session()
        Entry.insert(meeiro_id=meeiro_id, entry_date=america_timezone.localize(datetime(2018, 10, 2, 1, 1)),
                     entry_type_id=entry_type_id, entry_value=100.0,
                     description='veneno', db_session=execute_session)

        Entry.insert(meeiro_id=meeiro_id, entry_date=america_timezone.localize(datetime(2018, 10, 1, 23, 58)),
                     entry_type_id=entry_type_id, entry_value=1520.0,
                     description='combustivel', db_session=execute_session)

        filters_ = Entry.get_filters_to_query_entry(db_session=execute_session,
                                                    filter_value=NumValueLimit(value=100.2,
                                                                               operation=Operation.LESS_THAN,
                                                                               use_equal=True)
                                                    )
        entries = Entry.get_entries(execute_session, filters_)
        self.assertEqual(len(entries), 1)
        expected_entry = entries[0]

        self.assertEqual(expected_entry.entry_type_id, entry_type_id)
        self.assertEqual(str(expected_entry.entry_date), str(america_timezone.localize(datetime(2018, 10, 2, 1, 1))))
        self.assertEqual(expected_entry.meeiro_id, meeiro_id)
        self.assertEqual(expected_entry.description, 'veneno')
        self.assertEqual(expected_entry.entry_value, 100.0)

    def test_get_entries__filter_by_entry_type__expected_correct_result(self):
        america_timezone = pytz.timezone('America/Sao_Paulo')

        connection = Connection('postgres', 'root', '127.0.0.1:5432', 'planting_manager_teste')
        session = connection.session()
        meeiro_id = create_meeiro(name='tadeu', cpf='55584447213', rg='50658045x')
        entry_despesas_id = create_entry_type('despesas', connection)
        entry_adiantamento_id = create_entry_type('adiantamentos', connection)
        session.expunge_all()
        session.close()

        execute_session = connection.session()
        Entry.insert(meeiro_id=meeiro_id, entry_date=america_timezone.localize(datetime(2018, 10, 2, 1, 1)),
                     entry_type_id=entry_despesas_id, entry_value=100.0,
                     description='veneno', db_session=execute_session)

        Entry.insert(meeiro_id=meeiro_id, entry_date=america_timezone.localize(datetime(2018, 10, 1, 23, 58)),
                     entry_type_id=entry_adiantamento_id, entry_value=1520.0,
                     description='adiantamento', db_session=execute_session)

        filters_ = Entry.get_filters_to_query_entry(db_session=execute_session,
                                                    entry_type_id=entry_despesas_id
                                                    )
        entries = Entry.get_entries(execute_session, filters_)
        self.assertEqual(len(entries), 1)
        expected_entry = entries[0]

        self.assertEqual(expected_entry.entry_type_id, entry_despesas_id)
        self.assertEqual(str(expected_entry.entry_date), str(america_timezone.localize(datetime(2018, 10, 2, 1, 1))))
        self.assertEqual(expected_entry.meeiro_id, meeiro_id)
        self.assertEqual(expected_entry.description, 'veneno')
        self.assertEqual(expected_entry.entry_value, 100.0)