from datetime import datetime, timedelta
from typing import Dict, Tuple
import iso8601
import re

__author__ = "Brian Schlining"
__copyright__ = "Copyright 2022, Monterey Bay Aquarium Research Institute"

__fmt = "%Y%m%dT%H%M%S.%fZ"

def compactIso(t: datetime) -> str:
    return t.strftime(__fmt)

def timebounds_for_media(media: Dict) -> Tuple[datetime, datetime]:
    start_time = iso8601.parse_date(media["start_timestamp"])
    dt = timedelta(milliseconds=media["duration_millis"])
    end_time = start_time + dt
    return (start_time, end_time)

def datetime_from_name(name: str) -> datetime:
    m = re.findall('\d{8}[T]\d{6,}', name)
    if m:
        d = m[-1]   
        if (len(d) > 15):
            d = d[:15] + '.' + d[15:]
        return iso8601.parse_date(d)
    m = re.findall('\d{14}', name)
    if m:
        d = m[-1][:8] + 'T' + m[-1][8:]
        return iso8601.parse_date(d)
    m = re.findall('\d{8}_\d{9}', name)
    if m:
        d = m[-1][:8] + "T" + m[-1][9:15] + "." + m[-1][15:]
        return iso8601.parse_date(d)
    raise RuntimeError(f'Failed to parse time from {name}')

