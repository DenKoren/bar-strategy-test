import unittest
from unittest_data_provider import data_provider

from bars import Bar
from datetime import date, time


class TestBarMethods(unittest.TestCase):
    bars_join = lambda: (
        (
            Bar(
                date(2018, 9, 12),
                time(20, 10),
                100,
                200,
                50,
                75,
                1
            ),
            Bar(
                date(2018, 9, 12),
                time(20, 11),
                110,
                240,
                60,
                130,
                1
            ),
        ),
        (
            Bar(
                date(2018, 9, 12),
                time(20, 9),
                110,
                240,
                60,
                130,
                1
            ),
            Bar(
                date(2018, 9, 12),
                time(20, 10),
                100,
                200,
                50,
                75,
                1
            ),
        ),
    )

    @data_provider(bars_join)
    def test_join(self, bar1, bar2):
        res = bar1.join(bar2)

        self.assertEqual(res.datetime, bar1.datetime, 'wrong result bar date')
        self.assertEqual(res.open, bar1.open, 'wrong result bar open')
        self.assertEqual(res.max, max(bar1.max, bar2.max), 'wrong result bar max')
        self.assertEqual(res.min, min(bar1.min, bar2.min), 'wront result bar min')
        self.assertEqual(res.close, bar2.close, 'wrong result bar close')
        self.assertEqual(res.scale, bar1.scale + bar2.scale, 'wrong result bar scale')


if __name__ == '__main__':
    unittest.main()
