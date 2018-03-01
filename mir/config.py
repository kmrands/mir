#!/usr/bin/env python

import os
import json


def find_root():
    working_dir = os.getcwd().split(os.sep)
    length = len(working_dir) + 1
    build_paths = filter(lambda x: x != '', ['/'.join(working_dir[:x]) for x in range(length)])
    paths = [x for x in reversed(build_paths)]
    for path in paths:
        test_root = os.path.join(path, '.mir')
        if os.path.isfile(test_root):
            return path
    return None


def get_config(root_dir):
    if root_dir:
        c = os.path.join(root_dir, '.mir')
        with open(c, 'r') as f:
            config = json.load(f)
        return config
    return None


ROOT_DIR = find_root()
MIR_DIR = os.path.realpath(__file__)
# CONFIG = get_config(ROOT_DIR)
