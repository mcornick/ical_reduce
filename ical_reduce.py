#!/usr/bin/env python3
# SPDX-License-Identifier: MIT

import copy
import datetime
import sys

import icalendar
import pytz


def ical_reduce(original_name, reduced_name):
    now = datetime.datetime.now(pytz.utc)
    reduced_cal = icalendar.Calendar()

    with open(original_name, "rb") as original:
        original_cal = icalendar.Calendar.from_ical(original.read())

    for event in original_cal.walk():
        if event.name == "VEVENT":
            start = event.decoded("dtstart")
            compare = copy.deepcopy(start)
            if type(compare) is datetime.date:
                compare = datetime.datetime.combine(
                    compare, datetime.datetime.min.time()
                )
            compare = compare.replace(tzinfo=pytz.utc)
            if compare > now:
                reduced_cal.add_component(event)

    with open(reduced_name, "wb") as reduced:
        reduced.write(reduced_cal.to_ical())


if __name__ == "__main__":
    original = sys.argv[1]
    reduced = sys.argv[2]
    ical_reduce(original, reduced)
