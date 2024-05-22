#!/usr/bin/python3
"""
Unit tests for the Place class
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlaceCreation(unittest.TestCase):
    """
    Tests for the instantiation of the Place class.
    """

    def setUp(self):
        try:
            os.rename("file.json", "temp_file.json")
        except FileNotFoundError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("temp_file.json", "file.json")
        except FileNotFoundError:
            pass

    def test_instance_creation_no_args(self):
        self.assertEqual(Place, type(Place()))

    def test_instance_stored_in_storage(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_type_is_str(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_type_is_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_type_is_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_class_attribute(self):
        place_instance = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(place_instance))
        self.assertNotIn("city_id", place_instance.__dict__)

    def test_user_id_class_attribute(self):
        place_instance = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(place_instance))
        self.assertNotIn("user_id", place_instance.__dict__)

    def test_name_class_attribute(self):
        place_instance = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(place_instance))
        self.assertNotIn("name", place_instance.__dict__)

    def test_description_class_attribute(self):
        place_instance = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(place_instance))
        self.assertNotIn("description", place_instance.__dict__)

    def test_number_rooms_class_attribute(self):
        place_instance = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(place_instance))
        self.assertNotIn("number_rooms", place_instance.__dict__)

    def test_number_bathrooms_class_attribute(self):
        place_instance = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(place_instance))
        self.assertNotIn("number_bathrooms", place_instance.__dict__)

    def test_max_guest_class_attribute(self):
        place_instance = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(place_instance))
        self.assertNotIn("max_guest", place_instance.__dict__)

    def test_price_by_night_class_attribute(self):
        place_instance = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(place_instance))
        self.assertNotIn("price_by_night", place_instance.__dict__)

    def test_latitude_class_attribute(self):
        place_instance = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(place_instance))
        self.assertNotIn("latitude", place_instance.__dict__)

    def test_longitude_class_attribute(self):
        place_instance = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(place_instance))
        self.assertNotIn("longitude", place_instance.__dict__)

    def test_amenity_ids_class_attribute(self):
        place_instance = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(place_instance))
        self.assertNotIn("amenity_ids", place_instance.__dict__)

    def test_unique_ids_for_different_instances(self):
        place_instance1 = Place()
        place_instance2 = Place()
        self.assertNotEqual(place_instance1.id, place_instance2.id)

    def test_different_created_at_for_instances(self):
        place_instance1 = Place()
        sleep(0.05)
        place_instance2 = Place()
        self.assertLess(place_instance1.created_at, place_instance2.created_at)

    def test_different_updated_at_for_instances(self):
        place_instance1 = Place()
        sleep(0.05)
        place_instance2 = Place()
        self.assertLess(place_instance1.updated_at, place_instance2.updated_at)

    def test_str_representation(self):
        current_date = datetime.today()
        current_date_repr = repr(current_date)
        place_instance = Place()
        place_instance.id = "777777"
        place_instance.created_at = place_instance.updated_at = current_date
        place_str = place_instance.__str__()
        self.assertIn("[Place] (777777)", place_str)
        self.assertIn("'id': '777777'", place_str)
        self.assertIn("'created_at': " + current_date_repr, place_str)
        self.assertIn("'updated_at': " + current_date_repr, place_str)

    def test_unused_args(self):
        place_instance = Place(None)
        self.assertNotIn(None, place_instance.__dict__.values())

    def test_kwargs_instantiation(self):
        current_date = datetime.today()
        current_date_iso = current_date.isoformat()
        place_instance = Place(id="777", created_at=current_date_iso, updated_at=current_date_iso)
        self.assertEqual(place_instance.id, "777")
        self.assertEqual(place_instance.created_at, current_date)
        self.assertEqual(place_instance.updated_at, current_date)

    def test_none_kwargs_instantiation(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlaceSaveMethod(unittest.TestCase):
    """
    Tests for the save method of the Place class.
    """

    def setUp(self):
        try:
            os.rename("file.json", "temp_file.json")
        except FileNotFoundError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("temp_file.json", "file.json")
        except FileNotFoundError:
            pass

    def test_single_save(self):
        place_instance = Place()
        sleep(0.05)
        first_updated_at = place_instance.updated_at
        place_instance.save()
        self.assertLess(first_updated_at, place_instance.updated_at)

    def test_multiple_saves(self):
        place_instance = Place()
        sleep(0.05)
        first_updated_at = place_instance.updated_at
        place_instance.save()
        second_updated_at = place_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        place_instance.save()
        self.assertLess(second_updated_at, place_instance.updated_at)

    def test_save_with_argument(self):
        place_instance = Place()
        with self.assertRaises(TypeError):
            place_instance.save(None)

    def test_save_updates_file(self):
        place_instance = Place()
        place_instance.save()
        place_instance_id = "Place." + place_instance.id
        with open("file.json", "r") as file:
            self.assertIn(place_instance_id, file.read())


class TestPlaceToDictMethod(unittest.TestCase):
    """
    Tests for the to_dict method of the Place class.
    """

    def setUp(self):
        try:
            os.rename("file.json", "temp_file.json")
        except FileNotFoundError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("temp_file.json", "file.json")
        except FileNotFoundError:
            pass

    def test_to_dict_returns_dict(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_keys(self):
        place_instance = Place()
        self.assertIn("id", place_instance.to_dict())
        self.assertIn("created_at", place_instance.to_dict())
        self.assertIn("updated_at", place_instance.to_dict())
        self.assertIn("__class__", place_instance.to_dict())

    def test_to_dict_includes_added_attributes(self):
        place_instance = Place()
        place_instance.middle_name = "Johnson"
        place_instance.my_number = 777
        self.assertEqual("Johnson", place_instance.middle_name)
        self.assertIn("my_number", place_instance.to_dict())

    def test_to_dict_datetime_str(self):
        place_instance = Place()
        place_dict = place_instance.to_dict()
        self.assertEqual(str, type(place_dict["id"]))
        self.assertEqual(str, type(place_dict["created_at"]))
        self.assertEqual(str, type(place_dict["updated_at"]))

    def test_to_dict_output(self):
        current_date = datetime.today()
        place_instance = Place()
        place_instance.id = "777777"
        place_instance.created_at = place_instance.updated_at = current_date
        expected_dict = {
            'id': '777777',
            '__class__': 'Place',
            'created_at': current_date.isoformat(),
            'updated_at': current_date.isoformat(),
        }
        self.assertDictEqual(place_instance.to_dict(), expected_dict)

    def test_to_dict_not_equal_dunder_dict(self):
        place_instance = Place()
        self.assertNotEqual(place_instance.to_dict(), place_instance.__dict__)

    def test_to_dict_with_argument(self):
        place_instance = Place()
        with self.assertRaises(TypeError):
            place_instance.to_dict(None)


if __name__ == "__main__":
    unittest.main()

