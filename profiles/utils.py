# -*- coding: utf-8 -*-
import os
import random
import string

from django.conf import settings

SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 25)

def code_generator(size=SHORTCODE_MIN, chars=string.ascii_lowercase + string.digits):
    """ Code generated to activate account """
    return ''.join(random.choice(chars) for _ in range(size))

def delete_file(path):
    """ Deletes file from filesystem """

    try:
        if os.path.isfile(path):
            os.remove(path)
    except FileNotFoundError:
        pass