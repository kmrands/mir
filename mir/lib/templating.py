import os
import json
import sys

from jinja2 import FileSystemLoader, Environment

# Utility Functions
# -------------------------------

def template_factory(data, template_file):
    templates_dir = os.path.abspath(os.path.join(template_file, os.pardir))
    helpers_file = os.path.join(templates_dir, 'plugins.py')

    # Create template env
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template(os.path.basename(template_file))

    if os.path.isfile(helpers_file):
        sys.path.insert(0, templates_dir)
        env.trim_blocks = True
        env.lstrip_blocks = True
        env.globals['plugins'] = __import__('plugins')

    # Render
    return template.render(data=data)
