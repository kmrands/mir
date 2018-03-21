#!/usr/bin/env python
"""
A factory for registering all blueprints as custom endpoints from the routes directory.
"""

import os
import importlib
import datetime

import jwt
import bcrypt

from flask import (
    Blueprint,
    send_from_directory,
    jsonify,
    request,
    current_app as app
)
from mir.lib.common import get_attribute_names
# Add additional default routes manually

admin_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'admin')
admin_static_dir = os.path.join(admin_dir, 'admin-assets')


# -------------------------------
# Blueprint Factory
# -------------------------------

def blueprint_factory(app):
    if (app.config.get('CREATE_ADMIN_APP', False)):
        @app.route('/admin/')
        def index():
            return send_from_directory(admin_dir, 'index.html')

        @app.route('/admin-assets/<path:filename>')
        def admin_assets(filename):
            return send_from_directory(admin_static_dir, filename)

    @app.route('/api/v1/authenticate', methods=['POST'])
    def auth():
        data = request.get_json()
        if data:
            username = data.get('username', None)
            password = data.get('password', None)

            accounts = app.data.driver.db['accounts']
            lookup = {'username': username}

            valid_account = accounts.find_one(lookup)
            valid_password = bcrypt.hashpw(
                password.encode('utf-8'),
                valid_account['password'].encode('utf-8')
            ) == valid_account['password'] if valid_account else None

            if valid_account and valid_password:
                token = jwt.encode({
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
                    'username': valid_account['username']
                }, app.config['SECRET_KEY'], algorithm='HS256')
                return jsonify({
                    'status': 200,
                    'username': valid_account['username'],
                    'token': token
                }), 200

        return jsonify({'status': 401}), 400


    blueprints_path = os.path.join(os.getcwd(), 'routes')
    blueprint_names = get_attribute_names(blueprints_path)
    blueprints = {name: getattr(importlib.import_module('routes.%s' % name), name) for name in blueprint_names}
    for k, v in blueprints.items():
        if k != 'root':
            app.register_blueprint(v, url_prefix='/%s' % k)
        else:
            app.register_blueprint(v)
