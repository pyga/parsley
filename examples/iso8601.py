import datetime
import pytz

from parsley import makeGrammar

# See www.ietf.org/rfc/rfc3339.txt

_iso_8601_definition = r"""
year = <digit{4}>:Y -> int(Y)
month = <digit{2}>:m -> int(m)
day = <digit{2}>:d -> int(d)

hour = <digit{2}>:H -> int(H)
minute = <digit{2}>:M -> int(M)
second = <digit{2}>:S -> int(S)
fraction = '.' <digit+>:frac -> int(float('0.' + frac) * 10 ** 6)

sign = ('-' -> -1) | ('+' -> 1)
numeric_offset = sign:s hour:h ':' minute:m -> FixedOffset(s * (h * 60 + m))
utc = 'Z' -> UTC
offset = utc | numeric_offset

naive_time = hour:h ':' minute:m ':' second:s (fraction | -> 0):ms
             -> time(h, m, s, ms)
time = naive_time:t offset:o -> t.replace(tzinfo=o)
date = year:y '-' month:m '-' day:d -> date(y, m, d)

datetime = date:d 'T' time:t -> datetime.combine(d, t)
"""


DateTimeParser = makeGrammar(
    _iso_8601_definition,
    {
        'FixedOffset': pytz.FixedOffset,
        'date': datetime.date,
        'time': datetime.time,
        'datetime': datetime.datetime,
        'UTC': pytz.UTC,
    },
)
