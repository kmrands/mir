#!/usr/bin/env python

"""
Shared application utility functions.
"""

import os
import importlib
from base64 import b64encode

import bcrypt

from flask import current_app as app

from mir.config import APP_DIR, HAS_PROJECT_ROOT

# -----------------------------------
# Factory Meta Programming Helpers
# -----------------------------------

def is_an_attribute_name(attributes_path, filename):
    if (
            os.path.isfile(os.path.join(attributes_path, filename))
            and filename.endswith('py')
            and not filename.startswith('__init__')
    ):
        return True
    else:
        return False


def get_attribute_names(models_path):
    return [name.split('.')[0] for name in os.listdir(models_path) if is_an_attribute_name(models_path, name)]


# -----------------------------------
# Decorators
# -----------------------------------

def register_hook(*args):
    def decorate(f):
        def wrapper(app):
            for event in args:
                e = getattr(app, event) if hasattr(app, event) else None
                if e is not None:
                    e += f
        return wrapper
    return decorate


# -----------------------------------
# General Helpers
# -----------------------------------

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def get_settings_dict():
    settings_module = None
    additional_settings_module = None

    settings_module = importlib.import_module('settings')
    try:
        additional_settings_module = importlib.import_module('deployment_settings')
    except:
        pass

    settings = {
        setting: getattr(settings_module, setting)
        for setting in dir(settings_module)
        if not setting.startswith('_')
    }
    if additional_settings_module:
        additional_settings = {
            setting: getattr(additional_settings_module, setting)
            for setting in dir(additional_settings_module)
            if not setting.startswith('_')
        }

        settings = merge_two_dicts(settings, additional_settings)

    return settings


def get_models():
    def process_auth(v):
        auth = {}
        for key, value in v.items():
            if key == 'authentication' and isinstance(value, basestring):
                v[key] = auth[value]
        return v

    def register_model(directory, model_name, is_default=False):
        name = model_name.split('.')[0]
        model_import = importlib.import_module(
            '%s.%s' % (directory, name)
        )
        if hasattr(model_import, 'model'):
            model = getattr(model_import, 'model')
            return {
                name: model
            }

    def create_domain(all_models):
        return {
            k: process_auth(v)
            for d in filter(lambda x: x, all_models)
            for k, v in d.items()
        }

    user_model_dir = os.path.join(APP_DIR, 'models')
    default_model_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'default_models'
    )

    all_models = [
        register_model(user_model_dir.split('/')[-1], item)
        for item in os.listdir(user_model_dir)
        if not item.startswith("__") and '.pyc' not in item
    ] + [
        register_model(
            'mir.lib.%s' % default_model_dir.split('/')[-1],
            item,
            is_default=True
        )
        for item in os.listdir(default_model_dir)
        if not item.startswith("__") and item not in os.listdir(user_model_dir) and '.pyc' not in item
    ]

    return create_domain(all_models)
