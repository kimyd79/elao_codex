# Access-log baseline fixtures

These fixtures are the non-production baseline data for parser regression tests.

## Safety

- IP addresses use RFC 5737 documentation ranges (`192.0.2.0/24`,
  `198.51.100.0/24`, and `203.0.113.0/24`).
- Hostnames use the reserved `.test` domain.
- No production cookie, token, user identifier, or internal hostname is present.
- Keep new fixtures synthetic or irreversibly anonymized.

## Files

- `apache_combined.log`: Apache-style access logs with response time in
  microseconds.
- `nginx_combined.log`: Nginx access logs with `$request_time` in seconds.
- `iis_w3c.log`: IIS W3C logs, including comment/header lines.
- `app_time_format_2.log`: application log lines with a full date and time.
- `apache_mixed_invalid.log`: valid and deliberately invalid Apache-style rows.
- `expected_results.json`: formats and expected counts/aggregates.

## Compressed variants

Gzip and ZIP fixtures must be generated from the plain files in a test temporary
directory. Binary copies are not committed because they can silently drift away
from their source fixture. Compression tests must compare the decompressed bytes
with the source fixture before parsing.

## Counting convention

`physical_line_count` includes every physical line. `comment_line_count` is the
number of format/header comments intentionally ignored by a parser.
`data_line_count` is the number of non-comment input records. For malformed
fixtures, `expected_parsed_count + expected_rejected_count` must equal
`data_line_count`.
