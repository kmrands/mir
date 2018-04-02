import io
import StringIO
import base64
import json

from PIL import Image, ImageFilter, ImageEnhance
import requests

from flask import Blueprint, send_file, current_app, jsonify, request
from eve.methods import getitem

# ---------------------------------
# Processing Factory
# ---------------------------------

def process(binary, format='JPEG', quality=95):
    def transform(funclist):
        transformed = None
        try:
            transformed = Image.open(io.BytesIO(binary))
        except:
            transformed = Image.open(binary)

        for func in funclist:
            transformed = func(transformed)

        output = io.BytesIO()
        transformed.save(output, format=format, quality=quality)
        output.seek(0)

        return output
    return transform

# ---------------------------------
# Transformation Functions
# ---------------------------------

def thumbnail(size):
    size = [int(i) for i in size.split(',')]
    def create(img):
        img.thumbnail(size)
        return img
    return create


def rotate(deg):
    deg = int(deg)
    def create(img):
        return img.rotate(deg)
    return create


def crop(
    w,
    h,
    vert_position='center',
    horiz_position='center',
    cover=True,
    contain=False
):
    valid_positions= [
        'top',
        'bottom',
        'left',
        'right',
        'center'
    ]
    # TODO: Implement crop function
    def create(img):
        return img
    return create


def blur(radius):
    radius = float(radius)
    def create(img):
        return img.filter(
            ImageFilter.GaussianBlur(radius=radius)
        )
    return create


def contrast(value):
    adj_value = float(value)
    def create(img):
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(adj_value)
        return img
    return create


def saturation(value):
    adj_value = float(value)
    def create(img):
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(adj_value)
        return img
    return create


def brightness(value):
    adj_value = float(value)
    def create(img):
        enhancer= ImageEnhance.Brightness(img)
        img = enhancer.enhance(adj_value)
        return img
    return create


def sharpness(value):
    adj_value = float(value)
    def create(img):
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(adj_value)
        return img
    return create

def flip(direction):
    adj_value = float(value)
    def create(img):
        if direction =='horizontal':
            return img.transpose(Image.FLIP_LEFT_RIGHT)
        if direction =='vertical':
            return img.transpose(Image.FLIP_TOP_BOTTOM)
        else:
            return img
    return create

# ---------------------------------
# Lookups and Utilities
# ---------------------------------

funcs = {
    'thumbnail': thumbnail,
    'rotate': rotate,
    'blur': blur,
    'contrast': contrast,
    'brightness': brightness,
    'saturation': saturation,
    'sharpness': sharpness,
    'flip': flip
}

formats = [
    'JPEG',
    'GIF',
    'PNG'
]

def get_value(val):
    out = None
    try:
        out = json.loads(value)
    except:
        out = val
    return out

# ---------------------------------
# Routing
# ---------------------------------

def init_image_manipulation_api(app):
    @app.route('/api/images/<_id>/', methods=["GET"])
    def images(_id):
        binary = None
        instructions = request.args
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
