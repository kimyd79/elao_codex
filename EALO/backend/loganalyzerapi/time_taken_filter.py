import math

from rest_framework.exceptions import ValidationError


def time_taken_filter(lower, upper, unit):
    """Search inputs are milliseconds; a single boundary is exclusive."""
    try:
        lower, upper = [
            None if value is None or str(value).strip() == '' else float(value)
            for value in (lower, upper)
        ]
    except (TypeError, ValueError):
        raise ValidationError('TimeTaken must be a non-negative number.')
    if any(value is not None and (not math.isfinite(value) or value < 0)
           for value in (lower, upper)):
        raise ValidationError('TimeTaken must be a non-negative number.')
    if lower is not None and upper is not None and lower > upper:
        raise ValidationError('TimeTaken start must not exceed end.')
    factor = 1000 if unit == 'D' else 0.001 if unit == 'T' else 1
    if lower is not None and upper is not None:
        return {'ftime_taken__range': (lower * factor, upper * factor)}
    if lower is not None:
        return {'ftime_taken__gt': lower * factor}
    if upper is not None:
        return {'ftime_taken__lt': upper * factor}
    return {}
