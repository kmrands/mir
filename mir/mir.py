# -*- coding: utf-8 -*-

"""Main module."""

from __future__ import unicode_literals

import os
import sys
import multiprocessing
import gunicorn.app.base
from gunicorn.six import iteritems

import bcrypt
from eve import Eve
from eve.auth import BasicAuth
from eve.io.mongo import Validator
from itsdangerous import Signer, BadSignature
from flask_cors import CORS

from lib.common import generate_token, get_settings_dict, get_models
from lib.hooks import hooks_factory
from lib.blueprints import blueprint_factory

# Set up Path for application
settings_path = os.path.join(os.getcwd())
sys.path.insert(0, settings_path)

# Get settings
settings = get_settings_dict()

# ------------------------------
# Initialize authentication
# ------------------------------


class BasicAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        accounts = app.data.driver.db['accounts']
        lookup = {'username': username}
        if allowed_roles:
            lookup['roles'] = {'$in': allowed_roles}
        account = accounts.find_one(lookup)

        if account and '_id' in account:
            try:
                s = Signer(app.config['SECRET_KEY'])
                s.unsign(password)
                if password == account["token"]:
                    if resource == 'accounts':
                        new_account = account
                        new_account["token"] = generate_token(app.config['SECRET_KEY'], username)
                        app.data.replace('accounts', account['_id'], new_account, account)

                        self.set_request_auth_value(account['username'])
                    return True
                else:
                    return False
            except BadSignature:
                pass

            if resource == 'accounts':
                self.set_request_auth_value(account['username'])
            return account and \
                bcrypt.hashpw(password.encode('utf-8'), account['password'].encode('utf-8')) == account['password']


class MetaValidation(Validator):
    def _validate__metadata(self, metadata, field, value):
        pass

# ------------------------------
# Initialize Application
# ------------------------------

def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def start_dev_app():
    # Set up Eve Application
    settings['DOMAIN'] = get_models()

    app = Eve(
        settings=settings,
        auth=BasicAuth,
        validator=MetaValidation,
    )

    CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
    hooks_factory(app)
    blueprint_factory(app)

    # Run with Gunicorn
    options = {
        'bind': '%s:%s' % ('127.0.0.1', '8080'),
        'workers': number_of_workers(),
        'reload': True
    }
    StandaloneApplication(app, options).run()

def start_app():
    # Set up Eve Application
    settings['DOMAIN'] = get_models()
    settings['PUBLIC_METHODS'] = ['GET']
    settings['PUBLIC_ITEM_METHODS'] = ['GET']

    app = Eve(
        settings=settings,
        auth=BasicAuth,
        validator=MetaValidation,
    )

    CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
    hooks_factory(app)
    blueprint_factory(app)

    # Run with Gunicorn
    options = {
        'bind': '%s:%s' % ('127.0.0.1', '8080'),
        'workers': number_of_workers()
    }
    StandaloneApplication(app, options).run()

def create_app():
    # Set up Eve Application
    settings['DOMAIN'] = get_models()
    settings['PUBLIC_METHODS'] = ['GET']
    settings['PUBLIC_ITEM_METHODS'] = ['GET']

    app = Eve(
        settings=settings,
        auth=BasicAuth,
        validator=MetaValidation,
    )

    CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
    hooks_factory(app)
    blueprint_factory(app)

    return app
