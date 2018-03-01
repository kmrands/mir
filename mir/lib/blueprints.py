#!/usr/bin/env python
"""
A factory for registering all blueprints as custom endpoints from the routes directory.
"""

import os
import importlib

from mir.lib.common import get_attribute_names
# Add additional default routes manually


# -------------------------------
# Blueprint Factory
# -------------------------------

def blueprint_factory(app):
    blueprints_path = os.path.join(os.getcwd(), 'routes')
    blueprint_names = get_attribute_names(blueprints_path)
    blueprints = {name: getattr(importlib.import_module('routes.%s' % name), name) for name in blueprint_names}
    for k, v in blueprints.items():
        if k != 'root':
            app.register_blueprint(v, url_prefix='%s' % k)
        else:
            app.register_blueprint(v)
