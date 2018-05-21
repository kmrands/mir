model = {
    "schema": {
        "title": {
            "type": "string",
            "regex": "^[a-z0-9]+(?:-[a-z0-9]+)*$",
            "required": True,
            "unique": True,
            "minlength": 0,
            "maxlength": 400,
            "_metadata": {
                "order": 1,
                "help": "May only contain alpha-numeric characters and dashes",
                "label": "Setting Key",
                "field": "slug"
            }
        },
        "setting_value": {
            "type": "list",
            "schema": {
                "type": "dict",
                "anyof": [
                    {
                        "schema": {
                            "key": {
                                "type": "string",
                                "nullable": True,
                                "_metadata": {
                                    "order": 1,
                                    "help": "",
                                    "label": "Key",
                                    "field": "string"
                                }
                            },
                            "value": {
                                "type": "string",
                                "nullable": True,
                                "_metadata": {
                                    "order": 2,
                                    "help": "",
                                    "label": "Value",
                                    "field": "string"
                                }
                            },
                            "template": {
                                "type": "string",
                                "default": "string_value",
                            }
                        },
                        "_metadata": {
                            "order": 1,
                            "help": "",
                            "label": "String",
                            "field": "dict"
                        }
                    },
                    {
                        "schema": {
                            "key": {
                                "type": "string",
                                "nullable": True,
                                "_metadata": {
                                    "order": 1,
                                    "help": "",
                                    "label": "Key",
                                    "field": "string"
                                }
                            },
                            "value": {
                                "type": "string",
                                "_metadata": {
                                    "order": 2,
                                    "help": "",
                                    "label": "Value",
                                    "field": "richtext"
                                }
                            },
                            "template": {
                                "type": "string",
                                "default": "richtext_value",
                            }
                        },
                        "_metadata": {
                            "order": 2,
                            "help": "",
                            "label": "Rich Text",
                            "field": "dict"
                        }
                    },
                    {
                        "schema": {
                            "key": {
                                "type": "string",
                                "nullable": True,
                                "_metadata": {
                                    "order": 1,
                                    "help": "",
                                    "label": "Key",
                                    "field": "string"
                                }
                            },
                            "value": {
                                "type": "string",
                                "_metadata": {
                                    "order": 2,
                                    "help": "",
                                    "label": "Value",
                                    "field": "textfield"
                                }
                            },
                            "template": {
                                "type": "string",
                                "default": "text_value",
                            }
                        },
                        "_metadata": {
                            "order": 3,
                            "help": "",
                            "label": "Text",
                            "field": "dict"
                        }
                    },
                    {
                        "schema": {
                            "key": {
                                "type": "string",
                                "nullable": True,
                                "_metadata": {
                                    "order": 1,
                                    "help": "",
                                    "label": "Key",
                                    "field": "string"
                                }
                            },
                            "value": {
                                "type": ["objectid", "string"],
                                "data_relation": {
                                    "resource": "sitemedia",
                                    "field": "_id",
                                    "embeddable": True
                                },
                                "nullable": True,
                                "_metadata": {
                                    "order": 2,
                                    "help": "",
                                    "label": "Value",
                                    "field": "imagefield"
                                }
                            },
                            "template": {
                                "type": "string",
                                "default": "image_value",
                            }
                        },
                        "_metadata": {
                            "order": 4,
                            "help": "",
                            "label": "Image",
                            "field": "dict"
                        }
                    },
                    {
                        "schema": {
                            "key": {
                                "type": "string",
                                "nullable": True,
                                "_metadata": {
                                    "order": 1,
                                    "help": "",
                                    "label": "Key",
                                    "field": "string"
                                }
                            },
                            "value": {
                                "type": "list",
                                "schema": {
                                    "type": "string",
                                    "_metadata": {
                                        "field": "string"
                                    }
                                },
                                "_metadata": {
                                    "order": 2,
                                    "help": "",
                                    "label": "Value",
                                    "field": "simplelist"
                                }
                            },
                            "template": {
                                "type": "string",
                                "default": "list_value",
                            }
                        },
                        "_metadata": {
                            "order": 5,
                            "help": "",
                            "label": "List",
                            "field": "dict"
                        }
                    },
                    {
                        "schema": {
                            "key": {
                                "type": "string",
                                "nullable": True,
                                "_metadata": {
                                    "order": 1,
                                    "help": "",
                                    "label": "Key",
                                    "field": "string"
                                }
                            },
                            "value": {
                                "type": "list",
                                "schema": {
                                    "type": "dict",
                                    "schema": {
                                        "key": {
                                            "type": "string",
                                            "_metadata": {
                                                "order": 1,
                                                "help": "",
                                                "label": "Sub Key",
                                                "field": "string"
                                            }
                                        },
                                        "value": {
                                            "type": "string",
                                            "_metadata": {
                                                "order": 2,
                                                "help": "",
                                                "label": "Sub Value",
                                                "field": "richtext"
                                            }
                                        }
                                    },
                                    "_metadata": {
                                        "field": "dict"
                                    }
                                },
                                "_metadata": {
                                    "order": 2,
                                    "help": "Help text for list example",
                                    "label": "Key/Value Store",
                                    "field": "list"
                                }
                            },
                            "template": {
                                "type": "string",
                                "default": "dict_value",
                            }
                        },
                        "_metadata": {
                            "order": 6,
                            "help": "",
                            "label": "Key/Value Store Rich Text",
                            "field": "dict"
                        }
                    },
                    {
                        "schema": {
                            "key": {
                                "type": "string",
                                "nullable": True,
                                "_metadata": {
                                    "order": 1,
                                    "help": "",
                                    "label": "Key",
                                    "field": "string"
                                }
                            },
                            "value": {
                                "type": "list",
                                "schema": {
                                    "type": "dict",
                                    "schema": {
                                        "key": {
                                            "type": "string",
                                            "_metadata": {
                                                "order": 1,
                                                "help": "",
                                                "label": "Sub Key",
                                                "field": "string"
                                            }
                                        },
                                        "value": {
                                            "type": "string",
                                            "_metadata": {
                                                "order": 2,
                                                "help": "",
                                                "label": "Sub Value",
                                                "field": "textfield"
                                            }
                                        }
                                    },
                                    "_metadata": {
                                        "field": "dict"
                                    }
                                },
                                "_metadata": {
                                    "order": 2,
                                    "help": "",
                                    "label": "Key/Value Store Plaintext",
                                    "field": "list"
                                }
                            },
                            "template": {
                                "type": "string",
                                "default": "dict_value_plaintext",
                            }
                        },
                        "_metadata": {
                            "order": 7,
                            "help": "",
                            "label": "Key/Value Store Plaintext",
                            "field": "dict"
                        }
                    }
                ],
                "_metadata": {
                    "order": 1,
                    "help": "",
                    "label": "Options",
                    "field": "flexible_content"
                }
            },
            "_metadata": {
                "order": 2,
                "help": "",
                "label": "Setting Values",
                "field": "list"
            }
        },
        "tags": {
            "type": "list",
            "schema": {
                "type": "string",
                "_metadata": {
                    "field": "string"
                }
            },
            "_metadata": {
                "order": 3,
                "help": "",
                "label": "Tags",
                "field": "simplelist"
            }
        }
    },
	"cache_control": "",
	"cache_expires": 0,
    "allowed_roles": [{"role": "superuser"}],
	"public_methods": ['GET'],
	"public_item_methods": ['GET'],
	"resource_methods": ["GET", "POST"],
	"item_methods": ["GET", "PUT", "PATCH", "DELETE"],
    "versioning": True,
    "hateoas": False,
    "pagination": False,
}
