#!/usr/bin/env python
"""
A factory for registering all blueprints as custom endpoints from the routes directory.
"""

import os
import importlib

from flask import Blueprint, send_from_directory

from mir.lib.common import get_attribute_names
# Add additional default routes manually

admin_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'admin')
admin_static_dir = os.path.join(admin_dir, 'admin-assets')


# -------------------------------
# Blueprint Factory
# -------------------------------

def blueprint_factory(app):
    @app.route('/admin/')
    def index():
        return send_from_directory(admin_dir, 'index.html')

    @app.route('/admin-assets/<path:filename>')
    def admin_assets(filename):
        return send_from_directory(admin_static_dir, filename)

    blueprints_path = os.path.join(os.getcwd(), 'routes')
    blueprint_names = get_attribute_names(blueprints_path)
    blueprints = {name: getattr(importlib.import_module('routes.%s' % name), name) for name in blueprint_names}
    for k, v in blueprints.items():
        if k != 'root':
            app.register_blueprint(v, url_prefix='%s' % k)
        else:
            app.register_blueprint(v)
