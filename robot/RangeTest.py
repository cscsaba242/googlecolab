import unittest
from Range import Range

class Test(unittest.TestCase):
    def testNoInvalidParams(self):
        r = Range()
        # start, end, interval, max_per_request
        self.assertEqual(list(r.rolling_pages(1, 88, 10, 5)), [1, 51, 88])

    def testInvalidInterval(self):
        r = Range()
        self.assertEqual(list(r.rolling_pages(0, 10, 15, 5)), [], "Interval (15) is bigger than diff (10), should return empty list")

    def testInvalidRequest(self):
        r = Range()
        result = list(r.rolling_pages(0, 10, 1, 50))
        self.assertEqual(len(result), 10, "If max_per_request * interval > diff, result list length = diff / interval")


if __name__ == '__main__':
    unittest.main()