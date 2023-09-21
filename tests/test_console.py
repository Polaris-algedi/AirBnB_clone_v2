#!/usr/bin/python3
"""
This module contains unit tests for the HBNBCommand class.
"""

import unittest
from console import HBNBCommand
from models import storage
from models.place import Place
import os


class TestHBNBCommand(unittest.TestCase):
    """
    This class contains unit tests for the HBNBCommand class.
    """

    def setUp(self):
        """
        This method sets up the testing environment.
        It is run before each test.
        """
        self.cons = HBNBCommand()

    def tearDown(self):
        """
        This method cleans up the testing environment.
        It is run after each test.
        """
        storage._FileStorage__objects.clear()
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_do_create(self):
        """
        This method tests the 'create' command of the HBNBCommand class.
        """
        self.cons.onecmd('create Place city_id="0001" user_id="0001" '
                         'name="My_little_house" number_rooms=4 '
                         'number_bathrooms=2 max_guest=10 price_by_night=300 '
                         'latitude=37.773972 longitude=-122.431297')

        obj = list(storage.all().values())
        obj = obj[0]

        self.assertIsInstance(obj, Place)
        self.assertEqual(obj.city_id, '0001')
        self.assertEqual(obj.user_id, '0001')
        self.assertEqual(obj.name, 'My little house')
        self.assertEqual(obj.number_rooms, 4)
        self.assertEqual(obj.number_bathrooms, 2)
        self.assertEqual(obj.max_guest, 10)
        self.assertEqual(obj.price_by_night, 300)
        self.assertEqual(obj.latitude, 37.773972)
        self.assertEqual(obj.longitude, -122.431297)
