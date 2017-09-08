#!/usr/bin/env python

from copy import deepcopy
from datetime import datetime, date
from icalendar import Calendar
from pytz import utc
from sys import argv

try:
    original_name = argv[1]
except IndexError:
    original_name = 'original.ics'
try:
    reduced_name = argv[2]
except IndexError:
    reduced_name = 'reduced.ics'

now = datetime.now(utc)
reduced_cal = Calendar()

with open(original_name, 'rb') as original:
    original_cal = Calendar.from_ical(original.read())

for event in original_cal.walk():
    if event.name == 'VEVENT':
        start = event.decoded('dtstart')
        compare = deepcopy(start)
        if type(compare) is date:
            compare = datetime.combine(compare, datetime.min.time())
        compare = compare.replace(tzinfo=utc)
        if compare > now:
            reduced_cal.add_component(event)

with open(reduced_name, 'w') as reduced:
    reduced.write(reduced_cal.to_ical())
