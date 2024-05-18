#!/usr/bin/python3
"""Defines unittests for models/base_model.py.

Unittest classes:
    TestBaseModel_int
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):

    def test_init(self):
        """
        Test for init
        """
        ba_model = BaseModel()
        self.assertIsNotNone(ba_model.id)
        self.assertIsNotNone(ba_model.created_at)
        self.assertIsNotNone(ba_model.updated_at)

    def test_save(self):
        """
        Test for save method
        """
        ba_model = BaseModel()
        initial_updated_at = ba_model.updated_at
        current_updated_at = ba_model.save()
        self.assertNotEqual(initial_updated_at, current_updated_at)

    def test_to_dict(self):
        """
        Test for to_dict method
        """
        bam = BaseModel()
        bam_dict = bam.to_dict()
        self.assertIsInstance(bam_dict, dict)

        self.assertEqual(bam_dict["__class__"], 'BaseModel')
        self.assertEqual(bam_dict['id'], bam.id)
        self.assertEqual(bam_dict['created_at'], bam.created_at.isoformat())
        self.assertEqual(bam_dict["updated_at"], bam.created_at.isoformat())

    def test_str(self):
        """
        Test for string representation
        """
        ba_model = BaseModel()
        self.assertTrue(str(ba_model).startswith('[BaseModel]'))
        self.assertIn(ba_model.id, str(ba_model))
        self.assertIn(str(ba_model.__dict__), str(ba_model))


if __name__ == "__main__":
    unittest.main()
