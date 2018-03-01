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
            "type": "string",
            "allowed": ["user", "admin", "superuser"],
            "default": "user"
        },
        "token": {
            "type": "string"
        }
    },
    "additional_lookup": {
        "url": "regex('[\\w]+')",
        "field": "username"
    },
    "datasource": {
        "projection": {
            "password": 0
        }
    },
    "cache_control": "",
    "cache_expires": 0,
    "auth_field": "owner",
    "public_methods": [],
    "public_item_methods": [],
    "resource_methods": ["GET"],
    "item_methods": ["PUT", "PATCH"],
    "versioning": False
}
