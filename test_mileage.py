# Lab 5, Part 1

import mileage
from mileage import MileageError
import sqlite3
from unittest import TestCase

class TestMileageDB(TestCase):

    test_db_url = 'test_miles.db'

    # The name of this method is important - the test runner will look for it
    def setUp(self):
        # Overwrite the mileage
        mileage.db_url = self.test_db_url
        # drop everything from the DB to always start with an empty database
        conn = sqlite3.connect(self.test_db_url)
        conn.execute('DELETE FROM miles')

        # Added test records

        conn.execute("INSERT INTO miles ('vehicle', 'total_miles') values(?, ?)", ('PURPLE', int(111),))
        conn.execute("INSERT INTO miles ('vehicle', 'total_miles') values(?, ?)", ('ORANGE', int(222),))
        conn.execute("INSERT INTO miles ('vehicle', 'total_miles') values(?, ?)", ('GREEN', int(333),))

        conn.commit()
        conn.close()

    # Modified tests below to allow vehicle name in upper case

    def test_add_new_vehicle(self):
        mileage.add_miles('Blue Car', 100)
        expected = { 'BLUE CAR': 100 }
        self.compare_db_to_expected(expected)

        mileage.add_miles('Green Car', 50)
        expected['GREEN CAR'] = 50
        self.compare_db_to_expected(expected)

    def test_increase_miles_for_vehicle(self):
        mileage.add_miles('Red Car', 100)
        expected = { 'RED CAR': 100 }
        self.compare_db_to_expected(expected)

        mileage.add_miles('Red Car', 50)
        expected['RED CAR'] = 100 + 50
        self.compare_db_to_expected(expected)

    def test_add_new_vehicle_no_vehicle(self):
        with self.assertRaises(Exception):
            mileage.add_miles(None, 100)

    def test_add_new_vehicle_invalid_new_miles(self):
        with self.assertRaises(MileageError):
            mileage.add_miles('Car', -100)
        with self.assertRaises(MileageError):
            mileage.add_miles('Car', 'abc')
        with self.assertRaises(MileageError):
            mileage.add_miles('Car', '12.def')

    # Test new vehicles test added to DB using upper case
    def test_add_new_vehicle_upper_case(self):
        mileage.add_miles('YeLlOw car', 100)
        expected = {'YELLOW CAR': 100}
        self.compare_db_to_expected(expected)

        mileage.add_miles('yellow car', 50)
        expected['YELLOW CAR'] = 100 + 50
        self.compare_db_to_expected(expected)

    # This is not a test method, instead, it's used by the test methods
    def compare_db_to_expected(self, expected):

        conn = sqlite3.connect(self.test_db_url)
        cursor = conn.cursor()
        all_data = cursor.execute('SELECT * FROM MILES').fetchall()

        print(expected)
        print()
        print(all_data)

        # Same rows in DB as entries in expected dictionary
        self.assertEqual(len(expected.keys()), len(all_data))

        for row in all_data:
            # Vehicle exists, and mileage is correct
            self.assertIn(row[0], expected.keys())
            self.assertEqual(expected[row[0]], row[1])

        conn.close()
