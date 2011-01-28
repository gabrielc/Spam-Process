#! /usr/bin/python
# vim:fileencoding=utf-8

from datetime import date
from mboxlister import mbox_lister
from mboxparser import path_info
from mboxparser import parse_mbox



x = mbox_process(...)

for mbox_processed in x:
    ...
    ...
    ...
    x.send('PARA TUDO!')



mbox_processor_error_dict = {
        0 : "OK"
        1 : "Erro do tipo 1"
}

def mbox_processor(process_date, quarters_path, fail_object=None):
    """
    mbox_processor(datetime.date, string) -> tuples (generator)
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
        try:
            returned_path = path_info(mailbox_path)
            if returned_path is None:
                yield ((mailbox_path, 1, mbox_processor_error_dict[1]))
                continue

            if mailbox_path.colision:
                mbox_message = parse_mbox(mailbox_path.path)
            else:
                mbox_message = parse_mbox(mailbox_path.path, "gzip.open")

            ...            

        except:
            continue
