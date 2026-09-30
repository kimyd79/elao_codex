from django.test import SimpleTestCase
from rest_framework.exceptions import ValidationError

from .time_taken_filter import time_taken_filter


class TimeTakenFilterTests(SimpleTestCase):
    def test_single_bounds_are_exclusive_and_convert_milliseconds(self):
        self.assertEqual(time_taken_filter('1.5', '', 'D'), {'ftime_taken__gt': 1500})
        self.assertEqual(time_taken_filter(None, '250', 'T'), {'ftime_taken__lt': 0.25})
        self.assertEqual(time_taken_filter('0', None, 'D'), {'ftime_taken__gt': 0})

    def test_both_bounds_include_endpoints_and_empty_means_no_filter(self):
        self.assertEqual(time_taken_filter('2', '2', 'D'), {'ftime_taken__range': (2000, 2000)})
        self.assertEqual(time_taken_filter('', None, 'D'), {})

    def test_invalid_or_reversed_bounds_are_rejected(self):
        for lower, upper in [('3', '2'), ('-1', ''), ('nan', ''), ('', 'abc')]:
            with self.subTest(lower=lower, upper=upper), self.assertRaises(ValidationError):
                time_taken_filter(lower, upper, 'D')
