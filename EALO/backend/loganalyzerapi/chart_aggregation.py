from django.db.models import Count
from django.db.models.functions import Concat, Substr


def status_timeline(queryset, timeline):
    """Aggregate once and assemble ordered status buckets in linear time."""
    fields = ('fdate', 'fhour', 'fminute', 'fsecond')[:int(timeline) + 1]
    rows = (
        queryset.order_by()
        .annotate(f_date=Concat(*fields), f_status=Substr('fstatus', 1, 1))
        .values('f_date', 'f_status')
        .annotate(status_count=Count('f_status'))
        .order_by('f_date')
    )
    buckets = {}
    for row in rows.iterator(chunk_size=4096):
        counts = buckets.setdefault(row['f_date'], [0, 0, 0, 0])
        # Preserve time buckets even when they contain only other status codes.
        if row['f_status'] in ('2', '3', '4', '5'):
            counts[int(row['f_status']) - 2] = row['status_count']
    return (list(buckets), *[[counts[i] for counts in buckets.values()] for i in range(4)])
