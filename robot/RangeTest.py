import unittest
from Range import Range

class Test(unittest.TestCase):
    def testSample1(self):
        r = Range()
        # start, end, interval, max_per_request
        self.assertEqual(list(r.rolling_pages(1, 88, 10, 5)), [1, 51, 88])

    def testTooBigInterval(self):
        r = Range()
        # start, end, interval, max_per_request
        self.assertEqual(list(r.rolling_pages(0, 10, 15, 5)), [])

    def testTooMuchRequest(self):
        r = Range()
        self.assertEqual(list(r.rolling_pages(0, 10, 1, 50)), [])


t = Test()
t.testSample1()
#t.testTooBigInterval()
#t.testTooMuchRequest()