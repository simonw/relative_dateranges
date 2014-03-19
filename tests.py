import unittest
import datetime

from relative_timeframes import parse_date, RelativeParseError

DEFAULT_TEST_DATE = datetime.date(2014, 3, 18)

class TestParseDate(unittest.TestCase):
    def assertParsesToRange(self, input, expected_start, expected_end, dt=None):
        dt = dt or DEFAULT_TEST_DATE
        range_start, range_end = map(str, parse_date(input, dt))
        self.assertEqual(range_start, expected_start, 'input = %s, expected start = %s, got %s' % (
            input, expected_start, range_start
        ))
        self.assertEqual(range_end, expected_end, 'input = %s, expected end = %s, got %s' % (
            input, expected_end, range_end
        ))

    def test_fails_correctly(self):
        for bad in ('this', 'is', 'bad', 'data'):
            self.assertRaises(RelativeParseError, parse_date, bad)

	def test_today(self):
		self.assertParsesToRange('today',
			'2014-03-18', '2014-03-18'
		)

	def test_this_day(self):
		self.assertParsesToRange('this_day',
			'2014-03-18', '2014-03-18'
		)

	def test_this_week(self):
		# Weeks start on Sunday
		self.assertParsesToRange('this_week',
			'2014-03-16', '2014-03-22'
		)

    def test_this_month(self):
        self.assertParsesToRange('this_month',
            '2014-03-01', '2014-03-31'
        )
        # Test for Feb
        self.assertParsesToRange('this_month',
            '2014-02-01', '2014-02-28',
            dt = datetime.date(2014, 2, 2)
        )
        # Test for Dec
        self.assertParsesToRange('this_month',
            '2014-12-01', '2014-12-31',
            dt = datetime.date(2014, 12, 12)
        )

    def test_this_year(self):
        self.assertParsesToRange('this_year',
            '2014-01-01', '2014-12-31'
        )

    def test_this_n_days(self):
        # That's the current day + X days
        self.assertParsesToRange('this_5_days',
            '2014-03-18', '2014-03-22'
        )
        self.assertParsesToRange('this_2_days',
            '2014-03-18', '2014-03-19'
        )

    def test_this_n_weeks(self):
        # Current week + X weeks
        self.assertParsesToRange('this_2_weeks',
            '2014-03-16', '2014-03-29'
        )
        self.assertParsesToRange('this_3_weeks',
            '2014-03-16', '2014-04-05'
        )

    def test_this_n_months(self):
        self.assertParsesToRange('this_2_months',
            '2014-03-01', '2014-04-30'
        )
        self.assertParsesToRange('this_3_months',
            '2014-03-01', '2014-05-31'
        )
        self.assertParsesToRange('this_12_months',
            '2014-03-01', '2015-02-28'
        )
        self.assertParsesToRange('this_37_months',
            '2014-03-01', '2017-03-31'
        )
        self.assertParsesToRange('this_2_months',
            '2014-12-01', '2015-01-31',
            dt = datetime.date(2014, 12, 31)
        )

    def test_this_x_years(self):
        self.assertParsesToRange('this_2_years',
            '2014-01-01', '2015-12-31'
        )
        self.assertParsesToRange('this_5_years',
            '2014-01-01', '2018-12-31'
        )

    def test_tomorrow(self):
        self.assertParsesToRange('next_day',
            '2014-03-19', '2014-03-19'
        )
        self.assertParsesToRange('tomorrow',
            '2014-03-19', '2014-03-19'
        )
        self.assertParsesToRange('tomorrow',
            '2014-04-01', '2014-04-01',
            dt = datetime.date(2014, 3, 31)
        )

    def test_yesterday(self):
        self.assertParsesToRange('previous_day',
            '2014-03-17', '2014-03-17'
        )
        self.assertParsesToRange('yesterday',
            '2014-03-17', '2014-03-17'
        )
        self.assertParsesToRange('yesterday',
            '2014-03-31', '2014-03-31',
            dt = datetime.date(2014, 4, 1)
        )

    def test_next_x_days(self):
        self.assertParsesToRange('next_3_days',
            '2014-03-19', '2014-03-21'
        )
        self.assertParsesToRange('next_40_days',
            '2014-03-19', '2014-04-27'
        )

    def test_next_week(self):
        self.assertParsesToRange('next_week',
            '2014-03-23', '2014-03-29'
        )
        self.assertParsesToRange('next_week',
            '2015-01-04', '2015-01-10',
            dt = datetime.date(2014, 12, 31)
        )

    def test_next_month(self):
        self.assertParsesToRange('next_month',
            '2014-04-01', '2014-04-30'
        )
        self.assertParsesToRange('next_month',
            '2015-01-01', '2015-01-31',
            dt = datetime.date(2014, 12, 31)
        )

    def test_next_x_months(self):
        self.assertParsesToRange('next_2_months',
            '2014-04-01', '2014-05-31'
        )
        self.assertParsesToRange('next_2_months',
            '2015-01-01', '2015-02-28',
            dt = datetime.date(2014, 12, 31)
        )
        self.assertParsesToRange('next_15_months',
            '2014-04-01', '2015-06-30'
        )


if __name__ == "__main__":
    unittest.main()
