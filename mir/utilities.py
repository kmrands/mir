#!/usr/bin/env python

import os
import copy
import json
import string
import binascii
from subprocess import call, Popen, check_call, check_output, STDOUT

FNULL = open(os.devnull, 'w')

def generate_password(length=18):
    if not isinstance(length, int) or length < 8:
        raise ValueError("temp password must have positive length")

    chars = string.uppercase + string.lowercase + string.digits
    return "".join(chars[ord(c) % len(chars)] for c in os.urandom(length))


def generate_secret_key():
    key = os.urandom(24)
    return binascii.hexlify(key)


def run_call(cmd, verbose=False):
    if verbose:
        call(cmd.split())
    else:
        call(cmd.split(), stdout=FNULL, stderr=STDOUT)


def run_popen(cmd, cwd, verbose=False):
    if verbose:
        running = Popen(cmd.split(), cwd=cwd)
        running.wait()
    else:
        running = Popen(cmd.split(), cwd=cwd, stdout=FNULL, stderr=STDOUT)
        running.wait()


def hand_popen(cmd, cwd, verbose=False):
    if verbose:
        running = Popen(cmd.split(), cwd=cwd)
        return running
    else:
        running = Popen(cmd.split(), cwd=cwd, stdout=FNULL, stderr=STDOUT)
        return running


def run_check_call(cmd, verbose=False):
    if verbose:
        return check_call(cmd.split())
    else:
        return check_call(cmd.split(), stdout=FNULL, stderr=STDOUT)


def run_check_output(cmd, verbose=False):
    return check_output(cmd.split())


def translations(model):
    schema = model['schema']
    nested = copy.deepcopy(schema)
    if nested.get('slug', False):
        nested.pop('slug')

    if nested.get('published', False):
        nested.pop('published')

    nested['language'] = {
        "type": "string",
        "required": True,
        "minlength": 0,
        "maxlength": 400,
        "_metadata": {
            "order": 0,
            "help": "",
            "label": "Language Code",
            "field": "string"
        }
    }

    schema['translations'] = {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": nested,
            "_metadata": {
                "field": "dict"
            }
        },
        "_metadata": {
            "order": 9999999,
            "help": "",
            "label": "Translations",
            "field": "list"
        }
    }

    model['schema'] = schema
    return model
