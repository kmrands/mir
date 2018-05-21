model = {
    "schema": {
        "item": {
          "type": "media"
        },
        "title": {
            "type": "string"
        },
        "type": {
            "type": "string",
            "allowed": ["file", "video", "image"]
        },
        "tags": {
            "type": "list",
            "schema": {
                "type": "string",
                "_metadata": {
                    "field": "string"
                }
            }
        }
    },
    "item_url": "regex('[a-f0-9]{24}')"
}
