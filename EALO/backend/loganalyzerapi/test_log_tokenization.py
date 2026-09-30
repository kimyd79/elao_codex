"""Differential tests against the original shlex tokenization contract."""
import itertools
import random
import shlex
import unittest
from pathlib import Path
from unittest.mock import patch

from loganalyzerapi import parsers


class LogTokenizationTests(unittest.TestCase):
    def assert_matches_original(self, line):
        try:
            expected = shlex.split(line)
        except ValueError as error:
            with self.assertRaises(ValueError) as actual:
                parsers.split_log_fields(line)
            self.assertEqual(str(actual.exception), str(error), repr(line))
        else:
            self.assertEqual(parsers.split_log_fields(line), expected, repr(line))

    def test_quotes_escapes_whitespace_and_malformed_input(self):
        cases = [
            '', ' \t\r\n', 'one two', '"" \'\' plain',
            'before"quoted words"after', '"a""b"', "'a'\"b\"",
            '"single \' quote"', "'double \" quote'", "'back\\slash'",
            r'one\ two three', r'"a\"b"', r'"a\\b"', r'"a\qb"',
            'one\\', '"unclosed', "'unclosed", '"escaped\\',
            'a\vb\fc\u00a0d\u2003e', '"a\nb"\tc\r\nd',
            '#not-a-comment x#y ; | & ( )', '한글 "日本語 😀"',
            'a\0b', '"long ' + 'x' * 100000 + '"',
            'x' * 100000 + '"unterminated',
            ' ' * 100000 + '"unterminated',
            'plain' + ' ' * 100000 + '"unterminated',
        ]
        for line in cases:
            with self.subTest(line=line[:80]):
                self.assert_matches_original(line)

    def test_exhaustive_short_quote_and_escape_combinations(self):
        alphabet = ['a', ' ', '"', "'", '\\', '\t']
        for length in range(6):
            for chars in itertools.product(alphabet, repeat=length):
                self.assert_matches_original(''.join(chars))

    def test_seeded_mixed_fields_and_arbitrary_input(self):
        rng = random.Random(20260928)
        atoms = ['plain', '"GET /a b HTTP/1.1"', "'user agent'", '""',
                 "'a\\b'", r'escaped\ space', r'"a\"b"', 'a"b"c',
                 '한글', '#fragment', 'a\u00a0b']
        for _ in range(3000):
            self.assert_matches_original(''.join(
                rng.choice(atoms) + rng.choice([' ', '\t', '\r\n', ''])
                for _ in range(rng.randrange(1, 12))
            ))
        for _ in range(3000):
            self.assert_matches_original(''.join(
                rng.choice('abc012 \t\n\r\v\f\u00a0\'"\\#😀')
                for _ in range(rng.randrange(100))
            ))

    def test_all_log_fixtures_match_original(self):
        directory = Path(__file__).parent / 'testdata' / 'access_logs'
        for fixture in directory.glob('*.log'):
            with fixture.open(encoding='utf-8') as source:
                for line in source:
                    self.assert_matches_original(line.rstrip('\r\n'))

    def test_ordinary_logs_do_not_call_the_slow_parser(self):
        line = '127.0.0.1 - - [12/Aug/2026:00:00:00 +0900] "GET / HTTP/1.1" 200 12 "-" "Browser/1.0"'
        expected = shlex.split(line)
        with patch.object(parsers.shlex, 'split', side_effect=AssertionError('slow path')):
            self.assertEqual(parsers.split_log_fields(line), expected)

    def test_validation_results_and_error_messages_are_unchanged(self):
        formats = [
            ('apache', {'t': 0, 's': 1, 'b': 2, 'D': 3}, '[12/Aug/2026:00:00:00 200 12 1000'),
            ('nginx', {'$time_local': 0, '$status': 1, '$body_bytes_sent': 2, '$request_time': 3}, '[12/Aug/2026:00:00:00 200 12 0.001'),
            ('IIS-W3C', {'date': 0, 'time': 1, 'sc-status': 2, 'cs-bytes': 3, 'time-taken': 4}, '2026-08-12 00:00:00 200 12 1000'),
            ('IIS-NCSA', {'t': 0, 's': 1, 'b': 2, 'T': 3}, '[12/Aug/2026:00:00:00 200 12 1'),
        ]
        for kind, index, valid in formats:
            cases = [valid, valid + ' extra', valid.replace('200', '700'),
                     valid.replace('200', 'no-status'), valid.replace('12 ', 'bad '),
                     valid.replace('2026', 'bad-year'), valid + ' "unterminated',
                     valid + '\\', ' '.join(valid.split(' ')[:-1]) + ' bad-duration']
            for line in cases:
                with self.subTest(kind=kind, line=line):
                    actual = parsers.validate_log_line(line, kind, 'test', index, len(index))
                    with patch.object(parsers, 'split_log_fields', shlex.split):
                        expected = parsers.validate_log_line(line, kind, 'test', index, len(index))
                    self.assertEqual(actual, expected)
