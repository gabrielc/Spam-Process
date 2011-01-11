#! /usr/bin/python
# vim:fileencoding=utf-8

import os
import re
import datetime

# Path Error String
LOGFILE_PATH_ERROR = "filelog_path parameter must be a valid path to a \
spamsinkd logfile."


def logfile_mboxset(logfile_path):
    """
    logfile_mboxset(string logfile_path) -> set([String1, String2 ...])

    Return a Set of mailboxes (each of those as a string path) found in the
    spamsinkd logfile file found in the given string path. """

    # Checking the argument path
    if not os.path.isfile(logfile_path):
        raise TypeError(LOGFILE_PATH_ERROR)

    # Creating the set of mbox paths
    mbox_paths = set()

    # mbox attribute pattern, aiming: "mbox: path/to/mbox,"
    re_expr = re.compile('mbox: .*(mailstore[^,]+),')

    # Add to the set any mbox path found in every line of the logfile
    for line in open(logfile_path, 'r'):
        match = re_expr.search(line)
        if match:
            mbox_paths.add(match.group(1))

    return mbox_paths



def parse_logfile(logfile_path):
    """
    parse_logfile(string_logfilepath) -> [dict1(), dict2()...]

    Return an generator of dictionaries, each containing details of one line of
    a spamsinkd logfile file. Dictionary keys and values are determined
    dinamically based on every "Attribute: Value" pattern found in the line
    read. The dictionary usually takes the form: { Attribute1:Value1, ... }
    with "Attributes" and "Values" as string objects, except for the header
    contents and the "rcpts" attribute. If no header is found on a given line
    (this usually happens on malformed log lines), the dictionary will be
    returned empty.

    The header contents are stored in the following especial keys:
    ["header"]      --> string (full header information)
    ["logdatetime"] --> datetime object (log time in header)
    The "rcpts" attribute, when present, returns the list of recipients, as a
    list of tuples of strings, even when there is a single recipient. Each
    tuple represents an e-mail divided by the "@" character (although the "@"
    is aways ommited), in the form: (user, domain). For example
    "someone@something.com", would be returned as the tuple
    ('someone','something.com').
    """

    # The path must be valid
    if not os.path.isfile(logfile_path):
        raise TypeError(LOGFILE_PATH_ERROR)

    # This RE separates the header from the rest of the string
    re_expr_header = re.compile('^((\d+)\-(\d+)\-(\d+)\s+(\d\d)\:(\d\d)\:(\d\
\d)\s+\+\d\d\d\d\:\s+[^\:]+\:)(.*)')
    # This RE gets (iteratively) every basic log attribute from the string
    re_expr_attr = re.compile(r'\s([^\:]*)\: ([^\,]*),?')
    # This RE separates the "rcpts" attribute from the others
    re_expr_rcpt_att = re.compile(r'rcpts: (.+)(\s[^\@\:\s\,]*\:)?')
    # This RE get every rcpt from the "rcpts" attribute
    re_expr_rcpts = re.compile(r'([^\,\:\s]+)\@([^\,\:\s]+\.[^\,\:\s]+),?')

    for line in open(logfile_path, 'r'):
        match = re_expr_header.match(line)
        #print 'linha: ','"'+line+'"'
        if match:
            # Attributes dictionary
            attributes = dict()
            # Header special keys
            attributes['header'] = match.group(1)
            attributes['logdatetime'] = datetime.datetime(
                year = int(match.group(2)),
                month = int(match.group(3)),
                day = int(match.group(4)),
                hour = int(match.group(5)),
                minute = int(match.group(6)),
                second = int(match.group(7))
            )
            # Everything after the header
            string_attributes = match.group(8)
            # Searching for the other attributes (except rcpts):
            for match in re.finditer(re_expr_attr, string_attributes):
                if match.group(1) != 'rcpts':
                    attributes[match.group(1)] = match.group(2)

            # Searching for rcpts:
            match = re_expr_rcpt_att.search(string_attributes)
            if match:
                recipients = match.group(1)
                attributes['rcpts'] = list()
                # Get every recipient
                for match in re.finditer(re_expr_rcpts, recipients):
                    attributes['rcpts'].append((match.group(1),match.group(2)))
            # Yield the attributes
            yield attributes
        # No match for the header... yield an empty dictionary...
        else:
            yield(dict())
