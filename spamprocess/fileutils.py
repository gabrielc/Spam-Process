#! /usr/bin/python
# vim:fileencoding=utf-8

import os

def recursive_walk(path, maxdepth=-1, dirs_only=False, files_only=False):
    """ recursive_walk(string path, [maxdepth, dirs_only, files_only])
                                                        --> string (generator)

    Walks recursively from a given path, returning a generator of
    each file or directory string path found in the walk.

    If the maxdepth argument is non-negative, it defines the max amount of
    levels the walk may descend in the subdirectory tree beyond the
    initial path. maxdepth is negative by default.

    If dirs_only or files_only is true (false by default), it restricts the
    string paths returned, to only directories or files paths respectivly.
    """
    path = os.path.abspath(path)
    for file in [file for file in os.listdir(path) if not file in [".",".."]]:
            nfile = os.path.join(path,file)
            if os.path.isdir(nfile):
                if not files_only:
                    yield(nfile)
                if maxdepth != 0:
                    for generator in recursive_walk(nfile,
                                                    max([(maxdepth-1),-1]),
                                                    dirs_only, files_only):
                        yield(generator)
            else:
                if not dirs_only:
                    yield(nfile)
