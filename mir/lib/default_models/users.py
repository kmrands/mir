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
    "datasource": {
        "source": "accounts",
        "projection": {
            "token": 0,
            "password": 0
        }
    },
    "projection": False,
    "cache_control": "",
    "cache_expires": 0,
    "allowed_roles": [{"role": "superuser"}],
    "public_methods": [],
    "public_item_methods": [],
    "resource_methods": ["GET", "POST"],
    "item_methods": ["GET", "DELETE", "PATCH"],
    "versioning": False
}
