#!/usr/bin/env python
"""
A factory for registering all custom hooks from the hooks directory.
"""

import os
import json
import importlib
import inspect

import bcrypt
from flask import current_app

from mir.lib.common import register_hook, get_attribute_names


# -------------------------------
# Default Hooks
# -------------------------------

# Account Creation Hooks
@register_hook(
    'on_insert_person',
    'on_insert_users',
    'on_insert_accounts'
)
def account_creation(documents):
    for document in documents:
        if "password" in document:
            document["password"] = bcrypt.hashpw(
                document["password"].encode('utf-8'),
                bcrypt.gensalt()
            )
        document["owner"] = document["username"]
        current_app.logger.warning(
            'Account created: %s' % document["username"]
        )


@register_hook(
    'on_replace_person',
    'on_update_person',
    'on_replace_users',
    'on_update_users',
    'on_replace_accounts',
    'on_update_accounts'
)
def account_modification(item, original):
    current_app.logger.info(item)
    if 'password' in item:
        item["password"] = bcrypt.hashpw(
            item["password"].encode('utf-8'), bcrypt.gensalt()
        )
    item["owner"] = item["username"] \
        if "username" in item \
        else original["username"]


# Prevent 401 Dialog Hook
@register_hook('on_post_GET', 'on_post_POST', 'on_post_PUT', 'on_post_DELETE')
def fix_401(resource, request, payload):
    # Fix 401
    if payload.status_code == 401:
        payload.status_code = 400


# Schema info hook
def is_component(name):
    props = current_app.config['DOMAIN'][name]
    if 'hidden' in props and props['hidden']:
        return False
    return True


@register_hook('on_post_GET')
def info_schema(resource, request, payload):
    if request.endpoint is 'schema_collection':
        data = json.loads(payload.get_data().decode('utf-8'))
        resp = {k: v for k, v in data.items() if is_component(k)}
        payload.set_data(json.dumps(resp))


# -------------------------------
# Hooks Factory
# -------------------------------

def hooks_factory(app):
    hooks_path = os.path.join(os.getcwd(), 'hooks')
    hook_names = get_attribute_names(hooks_path)
    hook_modules = [
        importlib.import_module('hooks.%s' % name) for name in hook_names
    ]
    for module in hook_modules:
        listOfFunctions = [
            func_name for func_name, func in module.__dict__.items()
            if inspect.isfunction(func)
        ]
        for func in listOfFunctions:
            if func != 'register_hook':
                c = getattr(module, func)
                c(app)

    account_creation(app)
    info_schema(app)
    account_modification(app)
    fix_401(app)
