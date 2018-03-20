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
from eve.io.mongo.media import GridFSMediaStorage
from itsdangerous import Signer, BadSignature
from flask import current_app as app
from flask_cors import CORS
import jinja2

from lib.common import generate_token, get_settings_dict, get_models
from lib.hooks import hooks_factory
from lib.blueprints import blueprint_factory
from lib.bootstrap import create_admin
from lib.filestore import CloudinaryMediaStorage


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
                    return True
                else:
                    return False
            except BadSignature:
                pass

            if resource in app.config.get('OWNED_RESOURCES', []):
                self.set_request_auth_value(account['username'])
            return account and \
                bcrypt.hashpw(password.encode('utf-8'), account['password'].encode('utf-8')) == account['password']


class MetaValidation(Validator):
    def _validate__metadata(self, metadata, field, value):
        pass

# ------------------------------
# Initialize Application
# ------------------------------

def init_app(reload=False):
    # Set up Path for application
    settings_path = os.path.join(os.getcwd())
    sys.path.insert(0, settings_path)

    # Get settings
    settings = get_settings_dict()

    # Set up Media
    media = settings['MEDIA'] if 'MEDIA' in settings else GridFSMediaStorage

    # Set up Eve Application
    settings['DOMAIN'] = get_models()

    if not reload:
        settings['PUBLIC_METHODS'] = ['GET']
        settings['PUBLIC_ITEM_METHODS'] = ['GET']

    app = Eve(
        settings=settings,
        auth=BasicAuth,
        validator=MetaValidation,
        static_folder=os.path.join(settings_path, 'static'),
        media=media
    )
    create_admin(app, generate_token)

    template_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader([os.path.join(settings_path, 'templates')]),
    ])
    app.jinja_loader = template_loader

    CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
    hooks_factory(app)
    blueprint_factory(app)

    return app


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, initializer, reload, options=None):
        self.options = options or {}
        self.initializer = initializer
        self.reload = reload
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        app = self.initializer(self.reload)
        return app


def start_app(reload=False):

    # Run with Gunicorn
    options = {
        'bind': '%s:%s' % ('127.0.0.1', '8080'),
        'workers': 1 if reload else number_of_workers(),
        'reload': reload,
        'worker_class': 'gevent',
    }
    StandaloneApplication(init_app, reload, options).run()


def create_app():
    return init_app()
