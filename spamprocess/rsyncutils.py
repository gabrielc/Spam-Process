#! /usr/bin/python
# vim:fileencoding=utf-8

from re import search
from dateutils import date_from_iso
from os.path import basename
from fileutils import recursive_walk

RSYNC_PATTERN = "RSYNC_DONE"

def rsync_done_opener(main_path):
    """rsync_done_opener(string) --> array(file_descriptor)
    Receives an initial path to search for "rsync_done" files.
    Yields an array with such paths.
    Opens each path and returns an array with such opened files.""" 

    # Creates a list to store "rsync_done" files descriptor
    rsync_done_files = list()

    for file_path in recursive_walk(main_path, files_only=True):
        if basename(file_path) == RSYNC_PATTERN:
            # Opens each file
            try:
                rsync_done_files.append(open(file_path, "r"))
            except IOError:
                print >> stderr, "Invalid argument - [" + path + "] is not an openable file."
                continue

    return rsync_done_files


def rsync_done_reader(file_descriptor):
    """ rsync_done_reader(file) -> datetime.date(yyyy-mm-dd)
    Receives an "rsync_done" file. Once valid, returns the date found in it. """

    # Validates the argument 
    if not isinstance(file_descriptor, file):
        raise IOError, "Invalid argument - argument is not a file."
    if file_descriptor.mode.find('r') < 0:
        raise IOError, "Invalid argument - file must be readable."

    # Rewinds the file
    file_descriptor.seek(0)

    # Obtains date attributes - year, month and day
    line = file_descriptor.read()
    date_attributes = search("(\d{4})-(\d{2})-(\d{2})", line)

    if date_attributes is None:
        raise IOError, "Invalid argument - no valid date found."
    if len(date_attributes.groups()) != 3:
        raise IOError, "Invalid argument - no valid date found."

    # Returns a valid date
    valid_date = date_from_iso(date_attributes.group(0))

    return valid_date


def rsync_done_date(path):
    """rsync_done_date(string) -> date(yyyy-mm-dd)
    Receives a string with the initial path to search for "rsync_done" files.
    Reads each of the "rsync_done" files found, building an array of dates.
    Returns the earliest date among those found."""

    # Creates an array of dates
    dates = list()

    # Gets a date from each file opened
    for opened_file in rsync_done_opener(path):
        try:
            dates.append(rsync_done_reader(opened_file))
        except IOError:
            continue

    # Gets the earliest date in the array
    if dates:
        earliest_date = min(dates)
    else:
        earliest_date = ""

    return earliest_date
