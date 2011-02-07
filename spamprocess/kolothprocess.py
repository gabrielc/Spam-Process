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
            # to-do: yield ((mailbox_path, 2))
            continue

        if mailbox_path["compressed"]:
            mailbox_pack = parse_mbox(mailbox_path.path, gzip.open)
        else:
            mailbox_pack = parse_mbox(mailbox_path.path)

        for msg in mailbox_pack:
            feature_list = message_entries(msg.items(), STANDARD_ATTRIBUTES, STANDARD_FEATURES, EMPTY_FIELD, SEPARATOR)

    return



def message_entries(message_items, standard_attributes, standard_features, empty_field="NULL", separator="\t"):
    """
    message_entries(email.Message.items(), list(string), list(string), [string], [string]) -> string

        Walk through the 'standard_attributes' and 'standard_features' lists, looking for a match for
    every entry of them in the 'message_items' list.
        For every entry found, gets its position, and places its respective value in the vector 'message_values',
    on the exact position it was found in its original vector, except for the second vector items, that gets
    its values instilled in the vector 'message_values' on their former position, plus the size of the first
    vector checked -- standard_attributes.
        Once the vector has been compounded, it'll be filled with the values retrieved, and it may have some
    couple of entries corresponding to the value of the 'empty_field' argument -- due to the very creation of
    the vector, and to the fact that some values may not be found.
        Then, a string is written with the values recovered, but with some considerable specifications:

            - this part represents the attribute values
            - the string starts with the number of subsequent attribute values till another number come up
            - the value is separated from the first attribute value by a 'separator'
            - the attribute values are separated by a 'separator'
            pattern described:
                num_attribute_values, separator, attribute_value_1, separator, attribute_value_n, separator
                3\tattribute_value_1\tattribute_value_2\tattribute_value_3\t

            - the following part is regarded to the feature values
            - after the last 'separator' on the former part, -- which, in fact, is the last content of
            former part --, comes a number representing the quantity of subsequent feature values
            - the value is separated from the first feature value by a 'separator'
            - the feature values are separated by a 'separator'
            - the string ends when the 'num_feature_values' separator gets read
            pattern described:
                num_feature_values, separator, feature_value_1, separator, feature_value_n, separator
                3\tfeature_value_1\tfeature_value_2\tfeature_value_3\t

            - the entire string is about to look like:
                2\tattribute_value_1\tattribute_value_2\t2\tfeature_value_1\tfeature_value_2\t

        The string written is printed to the system.
    """

    attributes_size = len(standard_attributes)
    features_size = len(standard_features)
    message_values = [empty_field] * (attributes_size + features_size)

    for entry in message_items:

        # Here, the position starts from 0
        if standard_attributes.__contains__(message_items[entry][0]):
            position = standard_attributes.index(message_items[entry][0])
            message_values[position] = message_items[entry][1]

        # The position, in this part, starts from the size of the former array -- standard_attributes
        if standard_features.__contains__(message_items[entry][0]):
            position = attributes_size + standard_features.index(message_items[entry][0])
            message_values[position] = message_items[entry][1]


    # Creating the message_string
    message_string = ""

    message_string += str(attributes_size)
    message_string += separator

    for entry in message_values[:attributes_size]:
        message_string += (str(entry)+separator)

    message_string += str(features_size)
    message_string += separator

    for entry in message_values[attributes_size:]:
        message_string += (str(entry)+separator)

    print message_string

