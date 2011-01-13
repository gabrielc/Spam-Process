#! /usr/bin/python
# vim:fileencoding=utf-8

from dateutils import datequarter
from dateutils import date_from_iso
from fileutils import recursive_walk
from logfileparser import logfile_mboxset
from re import search
from re import compile
from os.path import basename
from datetime import date

def mbox_lister(search_date, quarters_path, fail_object=None):
    """mbox_lister(datetime.date, quarters_path, fail_object) --> Set([string_1, ..., string_n])
    Searches for mailboxes of a determined date received as argument.
    Returns a set with the path of such mailboxes."""

    # Verifies whether the type of the argument received is "date"
    if not isinstance(search_date, date):
        raise TypeError, "The argument \"search_date\" must be date typed;"

    # Gets the quarter which the date received belongs to
    quarter = datequarter(search_date) + 1

    # Compiling a regular expression to match the quarter in the path
    quarter_ex = compile(str(search_date.year)+"-Q"+str(quarter))

    # Search for a path that holds the calculated quarter
    for quarter_path in recursive_walk(quarters_path, maxdepth=0, dirs_only=True):
        if search(quarter_ex, quarter_path):
            break
        else:
            quarter_path = ""
    
    # Once there's no path within the determined quarter, returns the fail_object
    if quarter_path == "":
        return fail_object

    # Creates a list to store logfile paths
    logfile_list = list()

    # Search for logfiles produced in the received date
    for logfile_path in recursive_walk(quarter_path, files_only=True):
        if basename(logfile_path) == "logfile." + str(search_date):
            logfile_list.append(logfile_path)

    # Once there's no logfile path in the list, returns the fail_object
    if len(logfile_list) == 0:
        return fail_object

    # Creates a set to store mailbox paths
    mailbox_set = set()
    
    # Reads the logfiles formerly found in search of mailboxes
    for logfile_path in logfile_list:
        mailbox_set |= logfile_mboxset(logfile_path)

    return mailbox_set
