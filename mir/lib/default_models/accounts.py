model = {
    "schema": {
        "username": {
            "type": "string",
            "required": True,
            "unique": True,
            "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"
        },
        "password": {
            "type": "string",
            "required": True
        },
        "roles": {
            "type": "list",
            'schema': {
                'type': 'dict',
                'schema': {
                    'role': {
                        'type': 'string',
                        'default': 'superuser'
                    }
                }
            }
        }
    },
    "additional_lookup": {
        "url": "regex('[\\w]+')",
        "field": "username"
    },
    "datasource": {
        "projection": {
            "password": 0,
            "token": 0
        }
    },
    "projection": False,
    "cache_control": "",
    "cache_expires": 0,
    "auth_field": "owner",
    "public_methods": [],
    "public_item_methods": [],
    "resource_methods": ["GET"],
    "item_methods": ["PUT", "PATCH"],
    "versioning": False
}
