import unittest
from common import normalize_schedules
class TestCommonMethods(unittest.TestCase):
    def test_normalize_schedules(self):
        calendlySchedules = [('vc.sandeep11@gmail.com','19:00 Fri, 31 Jan 2020', 'New Event'), ('vc.sandeep11@gmail.com','','Canceled'), ('singhalamjeet18@gmail.com','19:30 Mon, 10 Feb 2020', 'New Event'), ('singhalamjeet18@gmail.com', '15:00 Sat, 8 Feb 2020', 'Updated')]
        result = normalize_schedules(calendlySchedules)
        self.assertEqual(result, [('singhalamjeet18@gmail.com', '15:00 Sat, 8 Feb 2020')])

if __name__ == '__main__':
    unittest.main()
