import unittest
from csf_db import DBSaver, fetch_count_and_day_lot, reset_count_and_day_lot
from csf_network import RequestSender


class DBTestCase(unittest.TestCase):
    def test_save(self):
        day_lot, count = fetch_count_and_day_lot()
        DBSaver(day_lot + 1, count + 1).run()
        updated_day_lot, updated_count = fetch_count_and_day_lot()
        self.assertEqual(day_lot + 1, updated_day_lot)
        self.assertEqual(count + 1, updated_count)

    def test_retrieve(self):
        reset_count_and_day_lot(1, 1)
        day_lot, count = fetch_count_and_day_lot()
        self.assertEqual(day_lot, 1)
        self.assertEqual(count, 1)


if __name__ == '__main__':
    unittest.main()
