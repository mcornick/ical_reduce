#!/usr/bin/env python3
# SPDX-License-Identifier: MIT

from copy import deepcopy
from datetime import date, datetime
from sys import argv

from icalendar import Calendar
from pytz import utc


def ical_reduce(original_name, reduced_name):
    now = datetime.now(utc)
    reduced_cal = Calendar()

    with open(original_name, "rb") as original:
        original_cal = Calendar.from_ical(original.read())

    for event in original_cal.walk():
        if event.name == "VEVENT":
            start = event.decoded("dtstart")
            compare = deepcopy(start)
            if type(compare) is date:
                compare = datetime.combine(compare, datetime.min.time())
            compare = compare.replace(tzinfo=utc)
            if compare > now:
                reduced_cal.add_component(event)

    with open(reduced_name, "wb") as reduced:
        reduced.write(reduced_cal.to_ical())


if __name__ == "__main__":
    try:
        original = argv[1]
    except IndexError:
        original = "original.ics"
    try:
        reduced = argv[2]
    except IndexError:
        reduced = "reduced.ics"
    ical_reduce(original, reduced)
