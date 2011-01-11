#! /usr/bin/python
# vim:fileencoding=utf-8

import os
import email
import datetime

# "mailstore" dir can be any directory used as a base path to contain mboxes in
# it or in subdirectories.
# The present implementation of spamsinkd by Cert stores mailboxes using
# this "mailstore" directory as a base path. If that changes,
# just modify this string to the new base dir.
MAILSTORE_DIR = 'mailstore'

def path_info(mbox_path, mailstore_path = None, not_found = None,
              targ_date_ip = False):
    """
    path_info(mbox_path, [maildirpath,][not_found_return]) -> dict()

    Search if there is a mbox file using the "mbox_path", even if the file
    was compressed (gziped). A dictionary containing information about the
    path and the file will be returned, or if no file is found, the
    "not_found" parameter will be returned (default to None).

    If "mailstore_path" is not None (the default) and it represents a valid
    path in the system, it will replace the begining of the "mbox_path" from
    root to the "mailstore" dir in the "mbox_path" for the search. This
    parameter is usefull mostly because the "mbox path" found in the logfiles
    are usually wrong until the "mailstore" dir, but the rest of the path is
    usually right. If no "mailstore" dir is found in mbox_path string, or if
    the "mailstore_path" is invalid, then the mbox_path parameter will be kept
    unchanged for the rest of the search.

    If the "targ_date_ip" parameter is True (default to False), information
    about the targ name and date will be recovered from the path string if
    possible. Note that this information may not be recovered and in those
    cases the dict returned will not have "targ", "date" and "ip" keys.

    If more than one file is found (compressed and not compressed), than the
    not compressed file will be evaluated and the returned dict key 'colision'
    will be True.

    The dictionary if returned have the following keys:

    path --> str (Path to the mailbox file. May be an .gz file!)
    compressed --> bool (True if the file found was compressed (gziped) and
                   has an .gz extension, otherwise returns False.)
    size --> long (Mbox file size in bytes.)
    colision --> bool (True if there is another mbox file with almost the same
                        name but ending with ".gz", otherwise returns False.)

    If "targ_date_ip" is True, then it MAY also have the following keys:

    targ --> str (Targ name information if found in the path string.)
    date --> datime.date (Date information if found in the path string.)
    ip --> str (Optional, ip information if found in the path string.)

    """
    if not mbox_path:
        return not_found

    # Okay, test if the path is a string (or if it can become one)
    if not isinstance(mbox_path,str):
        try:
            mbox_path = str(mbox_path)
        except:
            raise TypeError("mbox_path argument must be a mbox path string.")

    # If maildirpath is valid, use it to replace everything until the
    #  "mailstore" string of the mbox_path.
    mailstore_pos = mbox_path.find(MAILSTORE_DIR)
    if mailstore_path and os.path.isdir(mailstore_path) and mailstore_pos >= 0:
        if mailstore_path[-1] == '/':
            mailstore_path = mailstore_path[:-1]
        mbox_path = "/".join((mailstore_path,mbox_path[mailstore_pos+1+
                                                    len(MAILSTORE_DIR):]))

    def _get_targ_date_and_ip(str_path, mailstore_pos):
        """
        _get_targ_date_and_ip(str_path, mailstore_pos) -> tuple

        Returns the tuple (targ, date, ip) in this order in a tuple if
        possible, or else returns (None, None, None).

        targ and ip are returned as strings, date returns as a datetime.date
        object.

        """


        # Expected dir format:
        # "...mailstore/(year-quarter)/(ip_1)/(ip_2)/(ip_3)/(ip_4)/
        # (targ_name)/(iso-date)/(mbox)"
        # total of 8 important dirs
        # Anything but that cannot be used

        # If no mailstore in path...
        if mailstore_pos < 0:
            return ((None,None,None))
        # Split path string in a list of dirs
        str_path = str_path[mailstore_pos+len(MAILSTORE_DIR)+1:]
        dirs = str_path.split('/')
        # Must have 8 dirs:
        if len(dirs) != 8:
            return ((None,None,None))
        # Joining parts
        targ = dirs[5]
        date = dirs[6].split('-')
        if len(date) != 3:
            return ((None,None,None))
        date = datetime.date(date[0],date[1],date[2])
        ip = '.'.join(dirs[1],dirs[2],dirs[3],dirs[4])
        return ((targ,date,ip))



    # Now fill the file information in the following variables:
    path = ''
    compressed = False
    size = 0
    colision = False

    (targ,date,ip) = (None,None,None)

    # Try to find the file:
    if os.path.isfile(mbox_path):
        # Is the file compressed?
        if mbox_path[-3:] == '.gz':
            # There is a colision?
            if os.path.isfile(mbox_path[:-3]):
                path = mbox_path[:-3]
                colision = True
                compressed = False
                # TODO: get size
            else:
                path = mbox_path
                colision = False
                compressed = True
                # TODO: get size
        else:
            # There is a colision?
            if os.path.isfile(mbox_path+'.gz'):
                path = mbox_path
                colision = True
                compressed = False
                # TODO: get size
            else:
                path = mbox_path
                colision = False
                compressed = False
                # TODO: get size

    # Try to find the compressed file (with '.gz' at the end).
    elif os.path.isfile(mbox_path+'.gz'):
        path = mbox_path+'.gz'
        compressed = True
        # TODO: get size
        colision = False

    # If the path conatins .gz try to remove it
    elif mbox_path[-3:] == '.gz':
        if os.path.isfile(mbox_path[:-3]):
            path = mbox_path[:-3]
            compressed = False
            # TODO: get size
            colision = False
        else:
            # The file could not be found...
            return not_found
    else:
        # The file could not be found...
        return not_found

    if targ_date_ip:
        (targ,date,ip) = _get_targ_date_and_ip(mbox_path, mailstore_pos)

    return_dict = {
            'path' : path,
            'compressed' : compressed,
            'size' : size,
            'colision' : colision
        }

    if targ:
        return_dict['targ'] = targ
    if date:
        return_dict['date'] = date
    if ip:
        return_dict['ip'] = ip

    return return_dict


# ---------------------------------------------------------------------- #

def parse_mbox(mbox_path, open_function = open):
    """
    parse_mbox(string_path, [open_function = open]) -> mail.Message (generator)

    Iterates over the messages of a mbox file and return a Python email.Message
    Object (Generator, can be used in for loops). The optional second argument
    must be a callable function to be used to open the file (it must have
    similar interface to the default built in "open" command.)

    In the case of failure to open the file and read the contents an IOError
    exception will be raised. If there are problems with the file contents or
    if any argument have the wrong type, a TypeError exception will be raised
    with more details on the problem.

    """

    # Test the function arguments if they are ok...
    if not isinstance(mbox_path,str):
        try:
            mbox_path = str(mbox_path)
        except:
            raise TypeError("'mbox_path' argument must be a mbox path string.")

    if not callable(open_function):
        raise TypeError("'open_function' argument must be a callable object.")

    # Try to open the file... any problems the exceptions will be raised!
    mbox_file = open_function(mbox_path)

    # A blank line indicates that a new message may begin on mboxo format
    # fist_line tells us we dont have to deliver the last message
    last_line_blank = True
    first_line = True
    # MailParser can feed from the read lines and reconstruct the message
    MailParser = email.feedparser.FeedParser()
    for line in mbox_file:
        # If its the beginning of the file or last line was left blank
        # and the line begins with "From " then this is a
        # new message!
        if line[0:5] == 'From ' and last_line_blank:
            # If this is not the first line, return the last message
            if not first_line:
                # Return last message contents
                yield (MailParser.close())
                # Delete the last MessageParser reference (for the garbage
                # collector)
                del(MailParser)
                # Create a new MessageParser
                MailParser = email.feedparser.FeedParser()
            else:
                first_line = False
        else:
            if line in ['\n','\r','\r\n']:
                last_line_blank = True
            # Keep reading..
            #print "alimentei com : %s " % line
            MailParser.feed(line)
        #if line_number > 10000:
        #    break
    # If there is still one message to be delivered:
    last_message = MailParser.close()
    if last_message:
        yield (last_message)
    mbox_file.close()


def parse_test(mbox_set):
    """
    Função de teste... apague me assim que não for mais necessário...
    """

    print 'inicio...'
    now = datetime.datetime.now()
    counter = 0
    for message in mbox_messages(mbox_set):
        counter += 1
        #for key in message[0].keys():
            #print "%s: %s" % (key, message[0][key])
        #break
    time = datetime.datetime.now() - now
    print 'fim ->> %d time:  ' % counter  , time
