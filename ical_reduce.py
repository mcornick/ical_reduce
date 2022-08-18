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

    try:
        with open(original_name, "rb") as original:
            original_cal = icalendar.Calendar.from_ical(original.read())
    except FileNotFoundError:
        sys.stderr.write("{} not found\n".format(original_name))
        sys.exit(1)
    except IsADirectoryError:
        sys.stderr.write("{} is a directory\n".format(original_name))
        sys.exit(1)
    except PermissionError:
        sys.stderr.write("No permission to read {}\n".format(original_name))
        sys.exit(1)
    except OSError:
        sys.stderr.write("OS error trying to read {}\n".format(original_name))
        sys.exit(1)

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

    try:
        with open(reduced_name, "wb") as reduced:
            reduced.write(reduced_cal.to_ical())
    except IsADirectoryError:
        sys.stderr.write("{} is a directory\n".format(reduced_name))
        sys.exit(1)
    except PermissionError:
        sys.stderr.write("No permission to write {}\n".format(reduced_name))
        sys.exit(1)
    except OSError:
        sys.stderr.write("OS error trying to write {}\n".format(reduced_name))
        sys.exit(1)


if __name__ == "__main__":
    original = sys.argv[1]
    reduced = sys.argv[2]
    ical_reduce(original, reduced)
