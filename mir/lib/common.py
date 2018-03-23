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

def get_settings_dict():
    settings_module = None
    print os.getcwd()

    if not HAS_PROJECT_ROOT:
        settings_module = importlib.import_module('settings')
    else:
        settings_module = importlib.import_module('application.settings')

    settings = {
        setting: getattr(settings_module, setting)
        for setting in dir(settings_module)
        if not setting.startswith('_')
    }

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
        model = getattr(
            importlib.import_module(
                'application.%s.%s' % (directory, name)
            ), 'model'
        ) if not is_default and HAS_PROJECT_ROOT else getattr(
            importlib.import_module(
                '%s.%s' % (directory, name)
            ), 'model'
        )
        return {
            name: model
        }

    def create_domain(all_models):
        return {k: process_auth(v) for d in all_models for k, v in d.items()}

    user_model_dir = os.path.join(APP_DIR, 'models')
    default_model_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'default_models'
    )

    all_models = [
        register_model(user_model_dir.split('/')[-1], item)
        for item in os.listdir(user_model_dir)
        if not item.startswith("__")
    ] + [
        register_model(
            'mir.lib.%s' % default_model_dir.split('/')[-1],
            item,
            is_default=True
        )
        for item in os.listdir(default_model_dir)
        if not item.startswith("__")
    ]

    return create_domain(all_models)
