#! /usr/bin/python
# vim:fileencoding=utf-8

import datetime

def date_from_iso(iso_date_str):
    """ date_from_iso(iso_date_str) --> datetime.date

    Return a datetime.date representation of a date in iso string format.
    (Ex. "2010-12-23" --> datetime.date(2010,12,23)).
    """
    date_slices = iso_date_str.split("-")
    if len(date_slices) != 3:
        raise TypeError("The argument must be a string containing an iso\
 formated date.")
    try:
        date = datetime.date(int(date_slices[0]),
                             int(date_slices[1]),
                             int(date_slices[2]))
    except ValueError:
        raise TypeError("The argument must be a string containing an iso\
 formated, valid date.")

    return date


def datequarter(date):
    """ get_date_quarter(datetime.date) --> int

    Return the date quarter.
    """
    return (date.month-1)//3

def daterange(start_date, end_date):
    """
    daterange(datetime.date, datetime.date) --> datetime.date (generator)

    Iterates over the range of the given date span.
    """
    if start_date <= end_date:
        for n in range((end_date - start_date).days):
            yield start_date + datetime.timedelta(n)
        yield end_date
    else:
        for n in range((start_date - end_date).days):
            yield start_date - datetime.timedelta(n)
        yield end_date
