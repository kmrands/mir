from bson.son import SON

model = {
    "datasource": {
        "aggregation": {
            "pipeline": [
                {"$sort": SON([("_created", -1)])},
                {"$limit": 1}
            ]
        },
    },
    "allow_unknown": True,
	"cache_control": "",
	"cache_expires": 0,
	"allowed_roles": ["superuser", "admin"],
	"public_methods": ['GET'],
	"public_item_methods": [],
	"resource_methods": ["GET", "POST"],
	"item_methods": ["GET", "PUT", "PATCH", "DELETE"],
    "versioning": False
}
