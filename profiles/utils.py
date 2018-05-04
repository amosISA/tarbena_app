# -*- coding: utf-8 -*-
import os

def delete_file(path):
    # Deletes file from filesystem.
    try:
        if os.path.isfile(path):
            os.remove(path)
    except FileNotFoundError:
        print("Unable to remove file: %s" % path)