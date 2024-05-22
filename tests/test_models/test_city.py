#!/usr/bin/python3
"""
Module for City class unit tests
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class CityCreationTests(unittest.TestCase):
    """
    Tests for the instantiation of the City class.
    """

    def test_instance_creation_no_args(self):
        self.assertEqual(City, type(City()))

    def test_instance_stored_in_storage(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_type_check(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_type_check(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_type_check(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_class_attribute(self):
        city_instance = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(city_instance))
        self.assertNotIn("state_id", city_instance.__dict__)

    def test_name_class_attribute(self):
        city_instance = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(city_instance))
        self.assertNotIn("name", city_instance.__dict__)

    def test_unique_ids_for_different_instances(self):
        city_instance1 = City()
        city_instance2 = City()
        self.assertNotEqual(city_instance1.id, city_instance2.id)

    def test_created_at_for_different_instances(self):
        city_instance1 = City()
        sleep(0.05)
        city_instance2 = City()
        self.assertLess(city_instance1.created_at, city_instance2.created_at)

    def test_updated_at_for_different_instances(self):
        city_instance1 = City()
        sleep(0.05)
        city_instance2 = City()
        self.assertLess(city_instance1.updated_at, city_instance2.updated_at)

    def test_string_representation(self):
        current_date = datetime.today()
        current_date_repr = repr(current_date)
        city_instance = City()
        city_instance.id = "777777"
        city_instance.created_at = city_instance.updated_at = current_date
        city_str = city_instance.__str__()
        self.assertIn("[City] (777777)", city_str)
        self.assertIn("'id': '777777'", city_str)
        self.assertIn("'created_at': " + current_date_repr, city_str)
        self.assertIn("'updated_at': " + current_date_repr, city_str)

    def test_unused_args(self):
        city_instance = City(None)
        self.assertNotIn(None, city_instance.__dict__.values())

    def test_kwargs_instantiation(self):
        current_date = datetime.today()
        current_date_iso = current_date.isoformat()
        city_instance = City(id="345", created_at=current_date_iso, updated_at=current_date_iso)
        self.assertEqual(city_instance.id, "345")
        self.assertEqual(city_instance.created_at, current_date)
        self.assertEqual(city_instance.updated_at, current_date)

    def test_none_kwargs_instantiation(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class CitySaveTests(unittest.TestCase):
    """
    Tests for the save method of the City class.
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
        city_instance = City()
        sleep(0.05)
        first_updated_at = city_instance.updated_at
        city_instance.save()
        self.assertLess(first_updated_at, city_instance.updated_at)

    def test_double_save(self):
        city_instance = City()
        sleep(0.05)
        first_updated_at = city_instance.updated_at
        city_instance.save()
        second_updated_at = city_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        city_instance.save()
        self.assertLess(second_updated_at, city_instance.updated_at)

    def test_save_with_argument(self):
        city_instance = City()
        with self.assertRaises(TypeError):
            city_instance.save(None)

    def test_save_updates_file(self):
        city_instance = City()
        city_instance.save()
        city_id = "City." + city_instance.id
        with open("file.json", "r") as file:
            self.assertIn(city_id, file.read())


class CityToDictTests(unittest.TestCase):
    """
    Tests for the to_dict method of the City class.
    """

    def test_to_dict_returns_dict(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_keys(self):
        city_instance = City()
        self.assertIn("id", city_instance.to_dict())
        self.assertIn("created_at", city_instance.to_dict())
        self.assertIn("updated_at", city_instance.to_dict())
        self.assertIn("__class__", city_instance.to_dict())

    def test_to_dict_includes_added_attributes(self):
        city_instance = City()
        city_instance.middle_name = "Johnson"
        city_instance.my_number = 777
        self.assertEqual("Johnson", city_instance.middle_name)
        self.assertIn("my_number", city_instance.to_dict())

    def test_to_dict_datetime_str(self):
        city_instance = City()
        city_dict = city_instance.to_dict()
        self.assertEqual(str, type(city_dict["id"]))
        self.assertEqual(str, type(city_dict["created_at"]))
        self.assertEqual(str, type(city_dict["updated_at"]))

    def test_to_dict_output(self):
        current_date = datetime.today()
        city_instance = City()
        city_instance.id = "123456"
        city_instance.created_at = city_instance.updated_at = current_date
        expected_dict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': current_date.isoformat(),
            'updated_at': current_date.isoformat(),
        }
        self.assertDictEqual(city_instance.to_dict(), expected_dict)

    def test_to_dict_not_equal_dunder_dict(self):
        city_instance = City()
        self.assertNotEqual(city_instance.to_dict(), city_instance.__dict__)

    def test_to_dict_with_argument(self):
        city_instance = City()
        with self.assertRaises(TypeError):
            city_instance.to_dict(None)


if __name__ == "__main__":
    unittest.main()

