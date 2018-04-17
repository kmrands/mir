import io
import StringIO
import base64
import json

from PIL import Image, ImageFilter, ImageEnhance
import requests

from flask import Blueprint, send_file, current_app, jsonify, request
from cerberus import Validator
from eve.methods import getitem

from mir.lib.image_processing.transformations import funcs
from mir.lib.image_processing.factory import process
from mir.lib.image_processing.validation import schema


v = Validator()
v.allow_unknown = True

def is_image(item):
    if item.get('type', False) and item['type'] == 'image':
        return True
    return False

# ---------------------------------
# Routing
# ---------------------------------

def init_image_manipulation_api(app):
    @app.route('/api/images/<_id>/', methods=["GET"])
    def images(_id):
        binary = None
        instructions = request.args.to_dict()
        if v.validate(instructions, schema):
            # Setup file and content type
            media = getitem('sitemedia', **{'_id': _id})

            if 'file' in media[0]['item'] and isinstance(media[0]['item'], dict):
                f = media[0]['item']['file']
                content_type = media[0]['item']['content_type']

                # Create Binary
                binary = base64.b64decode(f)
            else:
                url = '%s%s' % (request.url_root, media[0]['item'][1:])
                r = requests.get(url, stream=True)
                if r.status_code == 200:
                    binary = r.raw
                    content_type = r.headers.get('content-type')

            # Create Processing Factory
            if binary and is_image(media[0]):
                processor = process(
                    binary,
                    format=instructions.get('format', 'JPEG'),
                    quality=instructions.get('quality', 95)
                )

                # Run Process Actions
                output = processor([
                    funcs[key](value) for key, value in instructions.iteritems() \
                    if funcs.get(key, False)
                ])


                # Return output
                return send_file(output, mimetype=content_type)
            elif binary and not is_image(media[0]):
                return send_file(io.BytesIO(binary), mimetype=content_type)
            else:
                return 'Not found', 404
        else:
            return jsonify({
                'status': 400,
                'msg': 'Query string is not valid for this endpoint',
                '_errors': v.errors
            }), 400


    @app.route('/api/images/external', methods=["GET"])
    def external():
        binary = None
        instructions = request.args.to_dict()
        url = instructions.get('url', None)
        if url:
            instructions.pop('url')
        if v.validate(instructions, schema) and url:
            # Setup file and content type
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                binary = r.raw
                content_type = r.headers.get('content-type')

            # Create Processing Factory
            if binary:
                processor = process(
                    binary,
                    format=instructions.get('format', 'JPEG'),
                    quality=instructions.get('quality', 95)
                )

                # Run Process Actions
                output = processor([
                    funcs[key](value) for key, value in instructions.iteritems() \
                    if funcs.get(key, False)
                ])


                # Return output
                return send_file(output, mimetype=content_type)
            else:
                return 'Not found', 404
        else:
            return jsonify({
                'status': 400,
                'msg': 'Query string is not valid for this endpoint',
                '_errors': v.errors
            }), 400
