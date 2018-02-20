# Lab 5, Part 1b

import mileage
import sqlite3
from unittest import TestCase

class TestMileageDBPart1b(TestCase):

    test_db_url = 'test_miles.db'

    # The name of this method is important - the test runner will look for it
    def setUp(self):
        # Overwrite the mileage
        mileage.db_url = self.test_db_url
        # drop everything from the DB to always start with an empty database
        conn = sqlite3.connect(self.test_db_url)
        conn.execute('DELETE FROM miles')

        # Add test records 

        conn.execute("INSERT INTO miles ('vehicle', 'total_miles') values(?, ?)", ('PURPLE', int(123),))
        conn.execute("INSERT INTO miles ('vehicle', 'total_miles') values(?, ?)", ('GREEN', int(223),))
        conn.execute("INSERT INTO miles ('vehicle', 'total_miles') values(?, ?)", ('ORANGE', int(112),))

        conn.commit()
        conn.close()

    def test_search_for_vehicle(self):
        testMe = mileage.search_for_vehicle('PURPLE')
        self.assertIn('PURPLE', testMe)
        self.assertNotIn('WHITE', testMe)

        # self.assertIn('Purple', testMe) fails
        # return None

        testMe = mileage.search_for_vehicle('Purple')   
        self.assertEqual(None, testMe)
