#!/usr/bin/python3
"""
Unit test module for the Review class
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReviewInitialization(unittest.TestCase):
    """
    Unit tests for initializing the Review class.
    """

    def test_instantiation_no_arguments(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instance_in_storage(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_string(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_class_attribute(self):
        review_instance = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(review_instance))
        self.assertNotIn("place_id", review_instance.__dict__)

    def test_user_id_is_class_attribute(self):
        review_instance = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(review_instance))
        self.assertNotIn("user_id", review_instance.__dict__)

    def test_text_is_class_attribute(self):
        review_instance = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(review_instance))
        self.assertNotIn("text", review_instance.__dict__)

    def test_unique_ids_for_different_instances(self):
        review1 = Review()
        review2 = Review()
        self.assertNotEqual(review1.id, review2.id)

    def test_different_created_at_for_instances(self):
        review1 = Review()
        sleep(0.05)
        review2 = Review()
        self.assertLess(review1.created_at, review2.created_at)

    def test_different_updated_at_for_instances(self):
        review1 = Review()
        sleep(0.05)
        review2 = Review()
        self.assertLess(review1.updated_at, review2.updated_at)

    def test_string_representation(self):
        current_date = datetime.today()
        current_date_repr = repr(current_date)
        review_instance = Review()
        review_instance.id = "777777"
        review_instance.created_at = review_instance.updated_at = current_date
        review_str = review_instance.__str__()
        self.assertIn("[Review] (777777)", review_str)
        self.assertIn("'id': '777777'", review_str)
        self.assertIn("'created_at': " + current_date_repr, review_str)
        self.assertIn("'updated_at': " + current_date_repr, review_str)

    def test_unused_args(self):
        review_instance = Review(None)
        self.assertNotIn(None, review_instance.__dict__.values())

    def test_kwargs_instantiation(self):
        current_date = datetime.today()
        current_date_iso = current_date.isoformat()
        review_instance = Review(id="777", created_at=current_date_iso, updated_at=current_date_iso)
        self.assertEqual(review_instance.id, "777")
        self.assertEqual(review_instance.created_at, current_date)
        self.assertEqual(review_instance.updated_at, current_date)

    def test_none_kwargs_instantiation(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReviewSaveMethod(unittest.TestCase):
    """
    Unit tests for the save method of the Review class.
    """

    @classmethod
    def setUp(cls):
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
        review_instance = Review()
        sleep(0.05)
        first_updated_at = review_instance.updated_at
        review_instance.save()
        self.assertLess(first_updated_at, review_instance.updated_at)

    def test_save_multiple_times(self):
        review_instance = Review()
        sleep(0.05)
        first_updated_at = review_instance.updated_at
        review_instance.save()
        second_updated_at = review_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        review_instance.save()
        self.assertLess(second_updated_at, review_instance.updated_at)

    def test_save_with_argument(self):
        review_instance = Review()
        with self.assertRaises(TypeError):
            review_instance.save(None)

    def test_save_updates_file(self):
        review_instance = Review()
        review_instance.save()
        review_id = "Review." + review_instance.id
        with open("file.json", "r") as file:
            self.assertIn(review_id, file.read())


class TestReviewToDictMethod(unittest.TestCase):
    """
    Unit tests for the to_dict method of the Review class.
    """

    def test_to_dict_returns_dict(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_keys(self):
        review_instance = Review()
        self.assertIn("id", review_instance.to_dict())
        self.assertIn("created_at", review_instance.to_dict())
        self.assertIn("updated_at", review_instance.to_dict())
        self.assertIn("__class__", review_instance.to_dict())

    def test_to_dict_includes_added_attributes(self):
        review_instance = Review()
        review_instance.middle_name = "Johnson"
        review_instance.my_number = 777
        self.assertEqual("Johnson", review_instance.middle_name)
        self.assertIn("my_number", review_instance.to_dict())

    def test_to_dict_datetime_str(self):
        review_instance = Review()
        review_dict = review_instance.to_dict()
        self.assertEqual(str, type(review_dict["id"]))
        self.assertEqual(str, type(review_dict["created_at"]))
        self.assertEqual(str, type(review_dict["updated_at"]))

    def test_to_dict_output(self):
        current_date = datetime.today()
        review_instance = Review()
        review_instance.id = "777777"
        review_instance.created_at = review_instance.updated_at = current_date
        expected_dict = {
            'id': '777777',
            '__class__': 'Review',
            'created_at': current_date.isoformat(),
            'updated_at': current_date.isoformat(),
        }
        self.assertDictEqual(review_instance.to_dict(), expected_dict)

    def test_to_dict_not_equal_dunder_dict(self):
        review_instance = Review()
        self.assertNotEqual(review_instance.to_dict(), review_instance.__dict__)

    def test_to_dict_with_argument(self):
        review_instance = Review()
        with self.assertRaises(TypeError):
            review_instance.to_dict(None)


if __name__ == "__main__":
    unittest.main()

