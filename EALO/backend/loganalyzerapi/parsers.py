"""Format-specific access-log validation shared by upload and analysis flows."""

import re
import shlex
from datetime import datetime


SUPPORTED_FORMATS = frozenset({'apache', 'nginx', 'IIS-W3C', 'IIS-NCSA', 'app'})


class FormatParser:
    format_kind = None

    def validate(self, line, format_name, format_index, expected_count):
        return validate_log_line(
            line, self.format_kind, format_name, format_index, expected_count
        )


class ApacheParser(FormatParser):
    format_kind = 'apache'


class NginxParser(FormatParser):
    format_kind = 'nginx'


class IISParser(FormatParser):
    format_kind = 'IIS-W3C'


class AppParser(FormatParser):
    format_kind = 'app'


PARSER_REGISTRY = {
    'apache': ApacheParser(),
    'nginx': NginxParser(),
    'IIS-W3C': IISParser(),
    'IIS-NCSA': IISParser(),
    'app': AppParser(),
}


def get_parser(format_kind):
    return PARSER_REGISTRY.get(format_kind)


def validate_log_line(line, format_kind, format_name, format_index, expected_count):
    if format_kind not in SUPPORTED_FORMATS:
        return ('unsupported_format', format_kind)
    if format_kind == 'app':
        patterns = {
            'time_format_1': (r'([0-9]{2}):([0-9]{2}):([0-9]{2})', '%H:%M:%S'),
            'time_format_2': (
                r'([0-9]{4})-([0-9]{2})-([0-9]{2}) '
                r'([0-9]{2}):([0-9]{2}):([0-9]{2})',
                '%Y-%m-%d %H:%M:%S',
            ),
        }
        pattern_info = patterns.get(format_name)
        if pattern_info is None:
            return ('unsupported_time_format', format_name)
        match = re.search(pattern_info[0], line)
        if match is None:
            return ('invalid_timestamp', 'Timestamp was not found')
        try:
            datetime.strptime(match.group(0), pattern_info[1])
        except ValueError as error:
            return ('invalid_timestamp', str(error))
        return None

    try:
        tokens = shlex.split(line)
    except ValueError as error:
        return ('invalid_quoting', str(error))
    if expected_count is not None and len(tokens) != expected_count:
        return ('field_count_mismatch', 'Expected %s fields but found %s' %
                (expected_count, len(tokens)))

    try:
        if format_kind == 'IIS-W3C':
            timestamp = '%s %s' % (tokens[format_index['date']], tokens[format_index['time']])
            datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        elif format_kind == 'nginx':
            datetime.strptime(tokens[format_index['$time_local']].lstrip('['), '%d/%b/%Y:%H:%M:%S')
        else:
            datetime.strptime(tokens[format_index['t']].lstrip('['), '%d/%b/%Y:%H:%M:%S')
    except (KeyError, IndexError, ValueError) as error:
        return ('invalid_timestamp', str(error))

    status_key, byte_key, duration_key = {
        'IIS-W3C': ('sc-status', 'cs-bytes', 'time-taken'),
        'nginx': ('$status', '$body_bytes_sent', '$request_time'),
    }.get(format_kind, ('s', 'b', 'D' if 'D' in format_index else 'T'))
    try:
        status_value = int(tokens[format_index[status_key]])
        if status_value < 100 or status_value > 599:
            raise ValueError('HTTP status is outside 100..599')
    except (KeyError, IndexError, ValueError) as error:
        return ('invalid_status', str(error))
    if byte_key in format_index:
        try:
            if tokens[format_index[byte_key]] != '-':
                int(tokens[format_index[byte_key]])
        except (IndexError, ValueError) as error:
            return ('invalid_bytes', str(error))
    if duration_key in format_index:
        try:
            float(tokens[format_index[duration_key]])
        except (IndexError, ValueError) as error:
            return ('invalid_duration', str(error))
    return None
