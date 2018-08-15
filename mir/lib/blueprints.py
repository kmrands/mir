#!/usr/bin/env python
"""
A factory for registering all blueprints as custom endpoints from the routes directory.
"""

import os
import io
import csv
import importlib
import datetime

import jwt
import bcrypt

from flask import (
    Blueprint,
    send_from_directory,
    jsonify,
    request,
    session,
    send_file,
    current_app as app
)
from eve.methods.get import get_internal

from mir.lib.common import get_attribute_names
from mir.lib.images import init_image_manipulation_api
from mir.lib.templating import template_factory
from mir.config import APP_DIR, HAS_PROJECT_ROOT
# Add additional default routes manually

admin_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'admin')
admin_static_dir = os.path.join(admin_dir, 'admin-assets')


# -------------------------------
# Blueprint Factory
# -------------------------------

def blueprint_factory(app):
    # Default Admin Routes
    if (app.config.get('CREATE_ADMIN_APP', False)):
        @app.route('/admin/')
        def index():
            return template_factory(
                {
                    'token': session.get('token', None),
                    'redirect': app.config.get('CUSTOM_AUTH_ENDPOINT', False)
                },
                os.path.join(admin_dir, 'index.html')
            )

        @app.route('/admin-assets/<path:filename>')
        def admin_assets(filename):
            return send_from_directory(admin_static_dir, filename)

    @app.route('/export/<resource>')
    def export(resource):
        token = request.headers.get("Authorization", None)
        authorized = app.auth.check_auth(token, None, None, "POST")
        domain = app.config.get('DOMAIN')
        schema = domain.get(resource, {})
        fieldnames = schema.get('schema', {}).keys()

        if not authorized:
            status_code = 400
            data = {
                "_error": {"code": 401, "message": "Please provide proper credentials"},
                "_status": "ERR",
            }
            return jsonify(data), status_code

        q = get_internal(resource)
        res = q[0] if len(q) > 0 else {}
        results = res.get('_items', None)
        if results and len(results) > 0:
            for item in results:
                item.pop('_links', None)
            csvfile = io.BytesIO()
            writer = csv.DictWriter(csvfile, fieldnames=list(set(results[0].keys() + fieldnames)))
            writer.writeheader()
            for item in results:
                writer.writerow(item)
            csvfile.seek(0)
            return send_file(csvfile, attachment_filename="export.csv")
        else:
            status_code = 404
            data = {
                "_error": {"code": 404, "message": "Resource not Found"},
                "_status": "ERR",
            }
            return jsonify(data), status_code

    # Image manipulation API
    if (app.config.get('CREATE_IMAGE_API', False)):
        init_image_manipulation_api(app)

    # Default Authentication Routes
    if not app.config.get('CUSTOM_AUTH', False):
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
                    }, app.config['SECRET_KEY'])

                    return jsonify({
                        'status': 200,
                        'username': valid_account['username'],
                        'roles': valid_account['roles'],
                        'token': token
                    }), 200

            return jsonify({'status': 401}), 400

    # Register Application Blueprints
    blueprints_path = os.path.join(APP_DIR, 'routes')
    blueprint_names = get_attribute_names(blueprints_path)
    module_import_string = lambda x: 'routes.%s' % x

    blueprints = {
        name: getattr(
            importlib.import_module(module_import_string(name)),
            name
        ) for name in blueprint_names
    }
    for k, v in blueprints.items():
        if k != 'root':
            app.register_blueprint(v, url_prefix='/%s' % k)
        else:
            app.register_blueprint(v)
