# ---------------------------------
# Validation Schema
# ---------------------------------

def to_bool(value):
    return value.lower() == 'true'

schema = {
    'format': {
        'type': 'string',
        'allowed': [
            'JPEG',
            'GIF',
            'PNG'
        ]
    },
    'quality': {
        'type': 'integer',
        'coerce': int
    },
    'optimize': {
        'type': 'boolean',
        'coerce': to_bool
    },
    'thumbnail': {
        'type': 'string',
        'regex': '^[0-9]+,[0-9]+$'
    },
    'rotate': {
        'type': 'integer',
        'coerce': int
    },
    'blur': {
        'type': 'float',
        'coerce': float
    },
    'contrast': {
        'type': 'float',
        'coerce': float
    },
    'brightness': {
        'type': 'float',
        'coerce': float
    },
    'saturation': {
        'type': 'float',
        'coerce': float
    },
    'sharpness': {
        'type': 'float',
        'coerce': float
    },
    'flip': {
        'type': 'string',
        'allowed': [
            'horizontal',
            'vertical',
        ]
    },
    'crop': {
        'type': 'string',
        'regex': '^[0-9]+,[0-9]+,\w+,\w+$'
    },
    'invert': {
        'type': 'boolean',
        'coerce': to_bool
    },
    'dotpattern': {
        'type': 'integer',
        'coerce': int
    }
}
