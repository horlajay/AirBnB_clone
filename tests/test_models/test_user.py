#!/usr/bin/python3
"""
Module for User class tests
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class UserInstantiationTests(unittest.TestCase):
    """
    Tests for the instantiation of User class.
    """

    def test_instance_creation_no_args(self):
        self.assertEqual(User, type(User()))

    def test_new_instance_in_storage(self):
        self.assertIn(User(), models.storage.all().values())

    def test_id_type(self):
        self.assertEqual(str, type(User().id))

    def test_created_at_type(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_type(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_email_type(self):
        self.assertEqual(str, type(User.email))

    def test_password_type(self):
        self.assertEqual(str, type(User.password))

    def test_first_name_type(self):
        self.assertEqual(str, type(User.first_name))

    def test_last_name_type(self):
        self.assertEqual(str, type(User.last_name))

    def test_unique_ids_for_different_users(self):
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)

    def test_created_at_for_different_users(self):
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.created_at, user2.created_at)

    def test_updated_at_for_different_users(self):
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.updated_at, user2.updated_at)

    def test_string_representation(self):
        date_now = datetime.today()
        date_repr = repr(date_now)
        user1 = User()
        user1.id = "777777"
        user1.created_at = user1.updated_at = date_now
        user_str = user1.__str__()
        self.assertIn("[User] (777777)", user_str)
        self.assertIn("'id': '777777'", user_str)
        self.assertIn("'created_at': " + date_repr, user_str)
        self.assertIn("'updated_at': " + date_repr, user_str)

    def test_unused_args(self):
        user1 = User(None)
        self.assertNotIn(None, user1.__dict__.values())

    def test_kwargs_instantiation(self):
        date_now = datetime.today()
        date_iso = date_now.isoformat()
        user1 = User(id="777", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(user1.id, "777")
        self.assertEqual(user1.created_at, date_now)
        self.assertEqual(user1.updated_at, date_now)

    def test_none_kwargs_instantiation(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class UserSaveTests(unittest.TestCase):
    """Tests for the save method of the User class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_single_save(self):
        user_instance = User()
        sleep(0.05)
        first_updated_at = user_instance.updated_at
        user_instance.save()
        self.assertLess(first_updated_at, user_instance.updated_at)

    def test_double_save(self):
        user_instance = User()
        sleep(0.05)
        first_updated_at = user_instance.updated_at
        user_instance.save()
        second_updated_at = user_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        user_instance.save()
        self.assertLess(second_updated_at, user_instance.updated_at)

    def test_save_with_argument(self):
        user_instance = User()
        with self.assertRaises(TypeError):
            user_instance.save(None)

    def test_save_updates_file(self):
        user_instance = User()
        user_instance.save()
        user_id = "User." + user_instance.id
        with open("file.json", "r") as file:
            self.assertIn(user_id, file.read())


class UserToDictTests(unittest.TestCase):
    """Tests for the to_dict method of the User class."""

    def test_to_dict_returns_dict(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_keys(self):
        user_instance = User()
        self.assertIn("id", user_instance.to_dict())
        self.assertIn("created_at", user_instance.to_dict())
        self.assertIn("updated_at", user_instance.to_dict())
        self.assertIn("__class__", user_instance.to_dict())

    def test_to_dict_includes_added_attributes(self):
        user_instance = User()
        user_instance.middle_name = "Holberton"
        user_instance.my_number = 98
        self.assertEqual("Holberton", user_instance.middle_name)
        self.assertIn("my_number", user_instance.to_dict())

    def test_to_dict_datetime_str(self):
        user_instance = User()
        user_dict = user_instance.to_dict()
        self.assertEqual(str, type(user_dict["id"]))
        self.assertEqual(str, type(user_dict["created_at"]))
        self.assertEqual(str, type(user_dict["updated_at"]))

    def test_to_dict_output(self):
        date_now = datetime.today()
        user_instance = User()
        user_instance.id = "777777"
        user_instance.created_at = user_instance.updated_at = date_now
        expected_dict = {
            'id': '777777',
            '__class__': 'User',
            'created_at': date_now.isoformat(),
            'updated_at': date_now.isoformat(),
        }
        self.assertDictEqual(user_instance.to_dict(), expected_dict)

    def test_to_dict_not_equal_dunder_dict(self):
        user_instance = User()
        self.assertNotEqual(user_instance.to_dict(), user_instance.__dict__)

    def test_to_dict_with_argument(self):
        user_instance = User()
        with self.assertRaises(TypeError):
            user_instance.to_dict(None)


if __name__ == "__main__":
    unittest.main()
