#!/usr/bin/python3
"""
Unit test module for the Amenity class
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenityInitialization(unittest.TestCase):
    """
    Unit tests for initializing the Amenity class.
    """

    def setUp(self):
        try:
            os.rename("file.json", "backup.json")
        except FileNotFoundError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("backup.json", "file.json")
        except FileNotFoundError:
            pass

    def test_instantiation_no_arguments(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_in_storage(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_string(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_class_attribute(self):
        amenity_instance = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", amenity_instance.__dict__)

    def test_unique_ids_for_different_instances(self):
        amenity1 = Amenity()
        amenity2 = Amenity()
        self.assertNotEqual(amenity1.id, amenity2.id)

    def test_different_created_at_for_instances(self):
        amenity1 = Amenity()
        sleep(0.05)
        amenity2 = Amenity()
        self.assertLess(amenity1.created_at, amenity2.created_at)

    def test_different_updated_at_for_instances(self):
        amenity1 = Amenity()
        sleep(0.05)
        amenity2 = Amenity()
        self.assertLess(amenity1.updated_at, amenity2.updated_at)

    def test_string_representation(self):
        current_date = datetime.today()
        current_date_repr = repr(current_date)
        amenity_instance = Amenity()
        amenity_instance.id = "777777"
        amenity_instance.created_at = amenity_instance.updated_at = current_date
        amenity_str = amenity_instance.__str__()
        self.assertIn("[Amenity] (777777)", amenity_str)
        self.assertIn("'id': '777777'", amenity_str)
        self.assertIn("'created_at': " + current_date_repr, amenity_str)
        self.assertIn("'updated_at': " + current_date_repr, amenity_str)

    def test_unused_args(self):
        amenity_instance = Amenity(None)
        self.assertNotIn(None, amenity_instance.__dict__.values())

    def test_kwargs_instantiation(self):
        current_date = datetime.today()
        current_date_iso = current_date.isoformat()
        amenity_instance = Amenity(id="777", created_at=current_date_iso, updated_at=current_date_iso)
        self.assertEqual(amenity_instance.id, "777")
        self.assertEqual(amenity_instance.created_at, current_date)
        self.assertEqual(amenity_instance.updated_at, current_date)

    def test_none_kwargs_instantiation(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenitySaveMethod(unittest.TestCase):
    """
    Unit tests for the save method of the Amenity class.
    """

    def setUp(self):
        try:
            os.rename("file.json", "backup.json")
        except FileNotFoundError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("backup.json", "file.json")
        except FileNotFoundError:
            pass

    def test_save_once(self):
        amenity_instance = Amenity()
        sleep(0.05)
        first_updated_at = amenity_instance.updated_at
        amenity_instance.save()
        self.assertLess(first_updated_at, amenity_instance.updated_at)

    def test_save_multiple_times(self):
        amenity_instance = Amenity()
        sleep(0.05)
        first_updated_at = amenity_instance.updated_at
        amenity_instance.save()
        second_updated_at = amenity_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        amenity_instance.save()
        self.assertLess(second_updated_at, amenity_instance.updated_at)

    def test_save_with_argument(self):
        amenity_instance = Amenity()
        with self.assertRaises(TypeError):
            amenity_instance.save(None)

    def test_save_updates_file(self):
        amenity_instance = Amenity()
        amenity_instance.save()
        amenity_id = "Amenity." + amenity_instance.id
        with open("file.json", "r") as file:
            self.assertIn(amenity_id, file.read())


class TestAmenityToDictMethod(unittest.TestCase):
    """
    Unit tests for the to_dict method of the Amenity class.
    """

    def setUp(self):
        try:
            os.rename("file.json", "backup.json")
        except FileNotFoundError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("backup.json", "file.json")
        except FileNotFoundError:
            pass

    def test_to_dict_returns_dict(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_keys(self):
        amenity_instance = Amenity()
        self.assertIn("id", amenity_instance.to_dict())
        self.assertIn("created_at", amenity_instance.to_dict())
        self.assertIn("updated_at", amenity_instance.to_dict())
        self.assertIn("__class__", amenity_instance.to_dict())

    def test_to_dict_includes_added_attributes(self):
        amenity_instance = Amenity()
        amenity_instance.middle_name = "Johnson"
        amenity_instance.my_number = 777
        self.assertEqual("Johnson", amenity_instance.middle_name)
        self.assertIn("my_number", amenity_instance.to_dict())

    def test_to_dict_datetime_str(self):
        amenity_instance = Amenity()
        amenity_dict = amenity_instance.to_dict()
        self.assertEqual(str, type(amenity_dict["id"]))
        self.assertEqual(str, type(amenity_dict["created_at"]))
        self.assertEqual(str, type(amenity_dict["updated_at"]))

    def test_to_dict_output(self):
        current_date = datetime.today()
        amenity_instance = Amenity()
        amenity_instance.id = "777777"
        amenity_instance.created_at = amenity_instance.updated_at = current_date
        expected_dict = {
            'id': '777777',
            '__class__': 'Amenity',
            'created_at': current_date.isoformat(),
            'updated_at': current_date.isoformat(),
        }
        self.assertDictEqual(amenity_instance.to_dict(), expected_dict)

    def test_to_dict_not_equal_dunder_dict(self):
        amenity_instance = Amenity()
        self.assertNotEqual(amenity_instance.to_dict(), amenity_instance.__dict__)

    def test_to_dict_with_argument(self):
        amenity_instance = Amenity()
        with self.assertRaises(TypeError):
            amenity_instance.to_dict(None)


if __name__ == "__main__":
    unittest.main()

