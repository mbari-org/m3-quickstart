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

# def datetime_from_name(name: str) -> datetime:
#     m = re.findall('\d{8}[T]\d{6,}', name)
#     if m:
#         d = m[-1]   
#         if (len(d) > 15):
#             d = d[:15] + '.' + d[15:]
#         return iso8601.parse_date(d)
#     m = re.findall('\d{14}', name)
#     if m:
#         d = m[-1][:8] + 'T' + m[-1][8:]
#         return iso8601.parse_date(d)
#     m = re.findall('\d{8}_\d{9}', name)
#     if m:
#         d = m[-1][:8] + "T" + m[-1][9:15] + "." + m[-1][15:]
#         return iso8601.parse_date(d)
#     m = re.search(r'(?P<year>\d{4})_(?P<month>\d{2})_(?P<day>\d{2})_(?P<hour>\d{2})_(?P<minute>\d{2})_(?P<second>\d{2})_(?P<millisec>\d{4})', name)
#     if m:
#         d = f"{m['year']}-{m['month']}-{m['day']}T{m['hour']}:{m['minute']}:{m['second']}.{m['millisec']}"
#         return iso8601.parse_date(d)
#     raise RuntimeError(f'Failed to parse time from {name}')


def datetime_from_name(name: str) -> datetime:
    # Case 1: Match full ISO 8601-like timestamps with optional fractional seconds
    m = re.findall(r'\d{8}[T]\d{6,}', name)
    if m:
        d = m[-1]   
        if len(d) > 15:
            d = d[:15] + '.' + d[15:]
        return iso8601.parse_date(d)
    
    # Case 2: Match compact YYYYMMDDHHMMSS format
    m = re.findall(r'\d{14}', name)
    if m:
        d = m[-1][:8] + 'T' + m[-1][8:]
        return iso8601.parse_date(d)
    
    # Case 3: Match YYYYMMDD_HHMMSSFFF format
    m = re.findall(r'\d{8}_\d{9}', name)
    if m:
        d = m[-1][:8] + "T" + m[-1][9:15] + "." + m[-1][15:]
        return iso8601.parse_date(d)
    
    # Case 4: Match structured format with underscores and fractional seconds
    m = re.search(r'(?P<year>\d{4})_(?P<month>\d{2})_(?P<day>\d{2})_(?P<hour>\d{2})_(?P<minute>\d{2})_(?P<second>\d{2})_(?P<millisec>\d{4})', name)
    if m:
        d = f"{m['year']}-{m['month']}-{m['day']}T{m['hour']}:{m['minute']}:{m['second']}.{m['millisec']}"
        return iso8601.parse_date(d)
    
    # Case 5: Match YYMMDD_HHMMSSFF format
    m = re.search(r'(?P<date>\d{6})_(?P<time>\d{8})', name)
    if m:
        date = m.group('date')
        time = m.group('time')
        year = int(date[:2]) + (2000 if int(date[:2]) < 70 else 1900)  # Adjust for YY to YYYY
        month = date[2:4]
        day = date[4:6]
        hour = time[:2]
        minute = time[2:4]
        second = time[4:6]
        fraction = time[6:8]
        d = f"{year}-{month}-{day}T{hour}:{minute}:{second}.{fraction}"
        return iso8601.parse_date(d)
    
    raise RuntimeError(f'Failed to parse time from {name}')


