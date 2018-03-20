model = {
    "schema": {},
    "datasource": {
        "filter": {
            "site": "mir"
        },
        "$limit": 1
    },
    "allow_unknown": True,
	"cache_control": "",
	"cache_expires": 0,
	"allowed_roles": ["superuser", "admin"],
	"public_methods": ['GET'],
	"public_item_methods": ['GET'],
	"resource_methods": ["GET"],
	"item_methods": ["GET", "PUT", "PATCH"],
    "versioning": True,
    "hateoas": False,
    "pagination": False,
}
