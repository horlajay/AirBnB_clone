#!/usr/bin/python3
"""
Module for State class unit tests
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class StateCreationTests(unittest.TestCase):
    """
    Tests for the instantiation of the State class.
    """

    def test_instance_creation_no_args(self):
        self.assertEqual(State, type(State()))

    def test_instance_stored_in_storage(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_type_check(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_type_check(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_type_check(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_class_attribute(self):
        st = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(st))
        self.assertNotIn("name", st.__dict__)

    def test_unique_ids_for_different_instances(self):
        st1 = State()
        st2 = State()
        self.assertNotEqual(st1.id, st2.id)

    def test_created_at_for_different_instances(self):
        st1 = State()
        sleep(0.05)
        st2 = State()
        self.assertLess(st1.created_at, st2.created_at)

    def test_updated_at_for_different_instances(self):
        st1 = State()
        sleep(0.05)
        st2 = State()
        self.assertLess(st1.updated_at, st2.updated_at)

    def test_string_representation(self):
        current_date = datetime.today()
        current_date_repr = repr(current_date)
        st = State()
        st.id = "777777"
        st.created_at = st.updated_at = current_date
        st_str = st.__str__()
        self.assertIn("[State] (777777)", st_str)
        self.assertIn("'id': '777777'", st_str)
        self.assertIn("'created_at': " + current_date_repr, st_str)
        self.assertIn("'updated_at': " + current_date_repr, st_str)

    def test_unused_args(self):
        st = State(None)
        self.assertNotIn(None, st.__dict__.values())

    def test_kwargs_instantiation(self):
        current_date = datetime.today()
        current_date_iso = current_date.isoformat()
        st = State(id="345", created_at=current_date_iso, updated_at=current_date_iso)
        self.assertEqual(st.id, "345")
        self.assertEqual(st.created_at, current_date)
        self.assertEqual(st.updated_at, current_date)

    def test_none_kwargs_instantiation(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class StateSaveTests(unittest.TestCase):
    """
    Tests for the save method of the State class.
    """

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp.json")
        except FileNotFoundError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("temp.json", "file.json")
        except FileNotFoundError:
            pass

    def test_single_save(self):
        st_instance = State()
        sleep(0.05)
        first_updated_at = st_instance.updated_at
        st_instance.save()
        self.assertLess(first_updated_at, st_instance.updated_at)

    def test_double_save(self):
        st_instance = State()
        sleep(0.05)
        first_updated_at = st_instance.updated_at
        st_instance.save()
        second_updated_at = st_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        st_instance.save()
        self.assertLess(second_updated_at, st_instance.updated_at)

    def test_save_with_argument(self):
        st_instance = State()
        with self.assertRaises(TypeError):
            st_instance.save(None)

    def test_save_updates_file(self):
        st_instance = State()
        st_instance.save()
        state_id = "State." + st_instance.id
        with open("file.json", "r") as file:
            self.assertIn(state_id, file.read())


class StateToDictTests(unittest.TestCase):
    """
    Tests for the to_dict method of the State class.
    """

    def test_to_dict_returns_dict(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_keys(self):
        st_instance = State()
        self.assertIn("id", st_instance.to_dict())
        self.assertIn("created_at", st_instance.to_dict())
        self.assertIn("updated_at", st_instance.to_dict())
        self.assertIn("__class__", st_instance.to_dict())

    def test_to_dict_includes_added_attributes(self):
        st_instance = State()
        st_instance.middle_name = "Johnson"
        st_instance.my_number = 777
        self.assertEqual("Johnson", st_instance.middle_name)
        self.assertIn("my_number", st_instance.to_dict())

    def test_to_dict_datetime_str(self):
        st_instance = State()
        st_dict = st_instance.to_dict()
        self.assertEqual(str, type(st_dict["id"]))
        self.assertEqual(str, type(st_dict["created_at"]))
        self.assertEqual(str, type(st_dict["updated_at"]))

    def test_to_dict_output(self):
        current_date = datetime.today()
        st_instance = State()
        st_instance.id = "777777"
        st_instance.created_at = st_instance.updated_at = current_date
        expected_dict = {
            'id': '777777',
            '__class__': 'State',
            'created_at': current_date.isoformat(),
            'updated_at': current_date.isoformat(),
        }
        self.assertDictEqual(st_instance.to_dict(), expected_dict)

    def test_to_dict_not_equal_dunder_dict(self):
        st_instance = State()
        self.assertNotEqual(st_instance.to_dict(), st_instance.__dict__)

    def test_to_dict_with_argument(self):
        st_instance = State()
        with self.assertRaises(TypeError):
            st_instance.to_dict(None)


if __name__ == "__main__":
    unittest.main()

