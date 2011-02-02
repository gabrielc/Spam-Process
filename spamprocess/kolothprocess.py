#! /usr/bin/python
# vim:fileencoding=utf-8

import email
from datetime import date
from mboxlister import mbox_lister
from mboxparser import path_info
from mboxparser import parse_mbox

def koloth_process(process_date, quarters_path, fail_object=None):
    """
    koloth_process(datetime.date, string) -> tuples (generator)
    Receives a date as argument and processes the mailboxes produced in such date.
    Returns a file with the elements yielded from the process.    
    """

    # Grants the date received to be iso formatted
    if not isinstance(process_date, date):
        raise TypeError, 'The argument "search_date" must be date typed;'
    
    # Search for mailboxes produced in the received date
    mbox_paths = mbox_lister(process_date, quarters_path)

    # Verifies if the set is empty
    if len(mbox_paths) == 0:
        return fail_object

    # Processes each mailbox from the set of mailbox paths
    for mailbox_path in mbox_paths:
        
        # Verifies if the mailbox exists and if it is compressed
        returned_path = path_info(mailbox_path)
       
        if returned_path is None:
            yield ((mailbox_path, 2))
            continue
        
        if mailbox_path["compressed"]:
            mailbox_pack = parse_mbox(mailbox_path.path, gzip.open)
        else:
            mailbox_pack = parse_mbox(mailbox_path.path)

        for msg in mailbox_pack:
            feature_list = message_features(msg.keys(), msg.values(), STANDARD_FEATURES, SEPARATOR)
            feature_store(feature_list)






def message_features(message_keys, message_values, standard_features, empty_field="NULL"):
    """
    message_features(email.Message.keys(), email.Message.values(), list(string), [string]) -> list(string)

        Walk through the 'standard_features', looking for every entry of this list in the 'message_keys' list.
        For every entry found, gets its position in the 'message_keys', which is the exact position of the
    determined key value in the 'message_values' list.
        Once the position has been retrieved, appends to a list named 'feature_list', the value in
    message_values[position].
        If there's no such 'feature_key' in the 'message_keys' list, appends to the 'feature_list' the
    'empty_field' value -- by default, set as "NULL".
        Returns the 'feature_list', yielded by the procedure.
    """

    feature_list = list()

    for feature_key in standard_features:
        if message_keys.__contains__(feature_key):
            position = message_keys.index(feature_key)
            feature_list.append(message_values[position])
        else:
            feature_list.append(empty_field)

    return feature_list




def feature_store(standard_features=None, feature_list=None, separator="\t", file_path="feature_store"):
    """
    feature_store([list(string)], [list(stuff)], [string], [string]) -> 

        Receives a list of features to be written on a determined file given by the 'file_path' argument.
        'file_path' equals 'feature_store' once no special path has been defined,
    
    Opens up a file or creates one, in order to write down the "feature"list receiveInserts the matching attributes and their determined values in the attribute_store argument,
    i.e., writes these parameters and values in a file according to the following pattern:
    attribute:value
    """

    
    












