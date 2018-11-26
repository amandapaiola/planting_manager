from unittest import TestCase

from models.exceptions import DuplicatedValue
from models.meeiro import Meeiro
from orm.planting import Meeiro as MeeiroMapping
from orm.postgres_connection import Connection
from tests.test_helper.test_helper import create_meeiro, initialize_database, clear_database, destroy_database


class MeeiroModelTest(TestCase):

    @classmethod
    def tearDownClass(cls):
        destroy_database()

    @classmethod
    def setUpClass(cls):
        initialize_database()

    def tearDown(self):
        clear_database()

    def test__get_meeiro_by_cpf__expect_correct_instance(self):
        connection = Connection('postgres', 'root', '127.0.0.1:5432', 'planting_manager_teste')
        create_meeiro(name='tadeu', cpf='55584447213', rg='50658045x')
        m = Meeiro.get_meeiro(connection.session(), cpf='55584447213')
        connection.session().close_all()

        self.assertEqual(m.name, 'tadeu')
        self.assertEqual(m.rg, '50658045x')

    def test__get_meeiro_by_cpf__expect_none(self):
        connection = Connection('postgres', 'root', '127.0.0.1:5432', 'planting_manager_teste')
        create_meeiro(name='tadeu', cpf='55584447213', rg='50658045x')

        m = Meeiro.get_meeiro(connection.session(), cpf='whatever')
        connection.session().close_all()

        self.assertIsNone(m)

    def test__insert_new_meeiro__expect_success(self):
        connection = Connection('postgres', 'root', '127.0.0.1:5432', 'planting_manager_teste')

        Meeiro.insert(connection.session(), cpf='whatever', rg='bla', name='lalala')
        connection.session().close_all()

        m = connection.session().query(MeeiroMapping).one()
        self.assertIsNotNone(m)
        self.assertEqual(m.cpf, 'whatever')
        self.assertEqual(m.rg, 'bla')
        self.assertEqual(m.name, 'lalala')

    def test__insert_meeiro_already_saved__expect_error(self):
        connection = Connection('postgres', 'root', '127.0.0.1:5432', 'planting_manager_teste')
        create_meeiro(name='tadeu', cpf='55584447213', rg='50658045x')
        connection.session().close_all()

        with self.assertRaises(DuplicatedValue):
            Meeiro.insert(connection.session(), name='tadeu', cpf='55584447213', rg='50658045x')

    def test__update_meeiro__expected_ok(self):
        connection = Connection('postgres', 'root', '127.0.0.1:5432', 'planting_manager_teste')
        meeiro_id = create_meeiro(name='tadeu', cpf='55584447213', rg='50658045x')
        connection.session().expunge_all()
        connection.session().close_all()

        result_set = Meeiro.update_meeiro(connection.session(), 'new_cpf', 'new_rg', 'new_name', meeiro_id)
        self.assertTrue(result_set)
        connection.session().expunge_all()
        connection.session().close_all()

        altered_obj = connection.session().query(MeeiroMapping).filter(MeeiroMapping.id == meeiro_id).one()
        self.assertEqual(altered_obj.name, 'new_name')
        self.assertEqual(altered_obj.rg, 'new_rg')
        self.assertEqual(altered_obj.cpf, 'new_cpf')

    def test__update_meeiro_cpf_already_saved_for_another__expected_ok(self):
        connection = Connection('postgres', 'root', '127.0.0.1:5432', 'planting_manager_teste')
        meeiro_id = create_meeiro(name='tadeu', cpf='55584447213', rg='50658045x')
        create_meeiro(name='another', cpf='1111111111', rg='2222222222')
        connection.session().expunge_all()
        connection.session().close_all()

        with self.assertRaises(DuplicatedValue):
            Meeiro.update_meeiro(connection.session(), new_cpf='1111111111', new_rg='new_rg',
                                 new_name='new_name', id_=meeiro_id)

    def test__update_meeiro_only_name__expected_ok(self):
        connection = Connection('postgres', 'root', '127.0.0.1:5432', 'planting_manager_teste')
        meeiro_id = create_meeiro(name='tadeu', cpf='55584447213', rg='50658045x')
        connection.session().expunge_all()
        connection.session().close_all()

        result_set = Meeiro.update_meeiro(connection.session(), new_cpf='55584447213',
                                          new_rg='50658045x', new_name='new_name', id_=meeiro_id)
        self.assertTrue(result_set)
        connection.session().expunge_all()
        connection.session().close_all()

        altered_obj = connection.session().query(MeeiroMapping).filter(MeeiroMapping.id == meeiro_id).one()
        self.assertEqual(altered_obj.name, 'new_name')
        self.assertEqual(altered_obj.rg, '50658045x')
        self.assertEqual(altered_obj.cpf, '55584447213')
