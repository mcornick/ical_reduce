#!/usr/bin/env python3
# SPDX-License-Identifier: MIT

"""Remove past events from an iCal calendar."""

# Copyright (c) 2017-2022 Mark Cornick
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import copy
import datetime
import sys

import click
import icalendar
import pytz


def ical_reduce(original, reduced):
    now = datetime.datetime.now(pytz.utc)
    reduced_cal = icalendar.Calendar()

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

    reduced.write(reduced_cal.to_ical())


@click.command()
@click.argument("original", type=click.File("r"))
@click.argument("reduced", type=click.File("w"))
def cli(original, reduced):
    """Remove past events from ORIGINAL and write to REDUCED."""
    ical_reduce(original, reduced)
