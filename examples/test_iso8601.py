import datetime
import unittest

try:
    import pytz
    from iso8601 import DateTimeParser
except ImportError:
    skip = 'pytz is not installed or usable'
else:
    skip = None


class TestDatetimeParsing(unittest.TestCase):
    if skip is not None:
        skip = skip

    def test_date(self):
        self.assertEqual(
            datetime.date(2001, 12, 25),
            DateTimeParser('2001-12-25').date())

    def test_naive_time(self):
        self.assertEqual(
            datetime.time(13, 59, 43),
            DateTimeParser('13:59:43').naive_time())

    def test_fractional_naive_time(self):
        self.assertEqual(
            datetime.time(13, 59, 43, 880000),
            DateTimeParser('13:59:43.88').naive_time())

    def test_utc_time(self):
        self.assertEqual(
            datetime.time(13, 59, 43, tzinfo=pytz.UTC),
            DateTimeParser('13:59:43Z').time())

    def test_fractional_utc_time(self):
        self.assertEqual(
            datetime.time(13, 59, 43, 880000, tzinfo=pytz.UTC),
            DateTimeParser('13:59:43.88Z').time())

    def test_timezone_time(self):
        self.assertEqual(
            datetime.time(13, 59, 43, tzinfo=pytz.FixedOffset(60)),
            DateTimeParser('13:59:43+01:00').time())

    def test_fractional_timezone_time(self):
        self.assertEqual(
            datetime.time(13, 59, 43, 770000, tzinfo=pytz.FixedOffset(60)),
            DateTimeParser('13:59:43.77+01:00').time())

    def test_numeric_offset(self):
        get_offset = lambda x: DateTimeParser(x).numeric_offset()
        self.assertEqual(pytz.FixedOffset(0), get_offset('+00:00'))
        self.assertEqual(pytz.FixedOffset(90), get_offset('+01:30'))
        self.assertEqual(pytz.FixedOffset(-150), get_offset('-02:30'))

    def test_datetime(self):
        self.assertEqual(
            datetime.datetime(
                2001, 12, 25, 13, 59, 43, 770000, tzinfo=pytz.UTC),
            DateTimeParser('2001-12-25T13:59:43.77Z').datetime())
