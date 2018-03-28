# -*- coding: utf-8 -*-

"""Main module."""

from __future__ import unicode_literals

import os
import sys
import multiprocessing
import gunicorn.app.base
from gunicorn.six import iteritems

import bcrypt
import jwt
import jinja2

from eve import Eve
from eve.auth import TokenAuth
from eve.io.mongo import Validator
from eve.io.mongo.media import GridFSMediaStorage
from flask import request, current_app as app
from flask_cors import CORS

from lib.common import get_settings_dict, get_models
from lib.hooks import hooks_factory
from lib.blueprints import blueprint_factory
from lib.bootstrap import create_admin
from lib.filestore import CloudinaryMediaStorage

from config import APP_DIR


# ------------------------------
# Initialize authentication
# ------------------------------

class jwtAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        # Patch, because what the fuck eve?
        # TODO: Why the fuck would eve make our token lowercase?
        token = request.headers.get('Authorization')
        if token:
            try:
                user_info = jwt.decode(
                    token,
                    app.config['SECRET_KEY']
                )
            except:
                user_info = {}

            username = user_info.get('username', None)
            accounts = app.data.driver.db['accounts']
            lookup = {'username': username}
            if resource and allowed_roles:
                lookup['roles'] = {'$in': allowed_roles}

            valid_account = accounts.find_one(lookup)
            if valid_account and '_id' in valid_account:
                if resource and resource in app.config.get('OWNED_RESOURCES', []):
                    self.set_request_auth_value(valid_account['username'])
                return True

        return False


class MetaValidation(Validator):
    # TODO: Build out metadata validation
    def _validate__metadata(self, metadata, field, value):
        pass

# ------------------------------
# Initialize Application
# ------------------------------

def init_app(reload=False):
    # Set up Path for application
    settings_path = os.path.join(APP_DIR)
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
        auth=jwtAuth,
        validator=MetaValidation,
        static_folder=os.path.join(settings_path, 'static'),
        media=media
    )
    create_admin(app)

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
    ip = '0.0.0.0'

    # Run with Gunicorn
    options = {
        'bind': '%s:%s' % (ip, '8080'),
        'workers': 1 if reload else number_of_workers(),
        'reload': reload,
        'worker_class': 'gevent',
    }
    StandaloneApplication(init_app, reload, options).run()


def create_app():
    return init_app()
