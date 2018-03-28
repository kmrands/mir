model = {
    "schema": {
        "string": {
            "type": "string",
            "minlength": 0,
            "maxlength": 300,
            "_metadata": {
                "order": 1,
                "help": "Help text for string example",
                "label": "String Field",
                "field": "string"
            }
        },
        "password": {
            "type": "string",
            "minlength": 0,
            "maxlength": 100,
            "_metadata": {
                "order": 1,
                "help": "Help text for password example",
                "label": "Password Field",
                "field": "password"
            }
        },
        "slug": {
            "type": "string",
            "minlength": 0,
            "maxlength": 400,
            "_metadata": {
                "order": 2,
                "help": "Help text for slug example",
                "label": "Slug Field",
                "field": "slug"
            }
        },
        "objectid": {
            "type": ["objectid", "string"],
            "data_relation": {
                "resource": "news",
                "field": "_id",
                "embeddable": True
            },
            "nullable": True,
            "_metadata": {
                "order": 8,
                "help": "Help text for relationship example",
                "label": "Relationship Field",
                "field": "objectid",
                "relationship": "news"
            }
        },
        "imagefield": {
            "type": ["objectid", "string"],
            "data_relation": {
                "resource": "media",
                "field": "_id",
                "embeddable": True
            },
            "nullable": True,
            "_metadata": {
                "order": 3,
                "help": "Help text for image example",
                "label": "Image Field",
                "field": "imagefield"
            }
        },
        "checklist": {
            "type": "list",
            "allowed": ["One", "Two", "Three"],
            "_metadata": {
                "order": 4,
                "help": "Help text for checklist example",
                "label": "Checklist Field",
                "field": "checklist",
                "choices": ["One", "Two", "Three"]
            }
        },
        "checkbox": {
            "type": "boolean",
            "_metadata": {
                "order": 5,
                "help": "Help text for checkbox example",
                "label": "Checkbox Field",
                "field": "checkbox"
            }
        },
        "dropdown": {
            "type": "string",
            "allowed": ["One", "Two"],
            "_metadata": {
                "order": 6,
                "help": "Help text for dropdown example",
                "label": "Dropdown Field",
                "field": "dropdown",
                "choices": ["One", "Two"]
            }
        },
        "radio": {
            "type": "string",
            "allowed": ["One", "Two"],
            "_metadata": {
                "order": 7,
                "help": "Help text for radio example",
                "label": "Radio Field",
                "field": "radio",
                "choices": ["One", "Two"]
            }
        },
        "richtext": {
            "type": "string",
            "_metadata": {
                "order": 8,
                "help": "Help text for richtext example",
                "label": "Rich Text Field",
                "field": "richtext"
            }
        },
        "simplelist": {
            "type": "list",
            "schema": {
                "type": "string",
                "_metadata": {
                    "field": "string"
                }
            },
            "_metadata": {
                "order": 9,
                "help": "Help text for list example",
                "label": "List Field",
                "field": "simplelist"
            }
        },
        "dict": {
            "type": "dict",
            "schema": {
                "item": {
                    "type": "string",
                    "_metadata": {
                        "order": 1,
                        "help": "sub-item string",
                        "label": "Dict Sub-item",
                        "field": "string"
                    }
                },
                "richtext": {
                    "type": "string",
                    "_metadata": {
                        "order": 8,
                        "help": "Help text for richtext example",
                        "label": "Rich Text Field",
                        "field": "richtext"
                    }
                }
            },
            "_metadata": {
                "order": 9,
                "help": "Help text for list example",
                "label": "Dict Field",
                "field": "dict"
            }
        },
        "listdict": {
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                    "item": {
                        "type": "string",
                        "_metadata": {
                            "order": 1,
                            "help": "sub-item string",
                            "label": "Dict Sub-item",
                            "field": "string"
                        }
                    },
                    "richtext": {
                        "type": "string",
                        "_metadata": {
                            "order": 8,
                            "help": "Help text for richtext example",
                            "label": "Rich Text Field",
                            "field": "richtext"
                        }
                    }
                },
                "_metadata": {
                    "field": "dict"
                }
            },
            "_metadata": {
                "order": 10,
                "help": "help",
                "label": "List of Dicts",
                "field": "list"
            }
        },
        "flexible_content": {
            "type": "dict",
            "anyof": [
                {
                    "schema": {
                        "item": {
                            "type": "string",
                            "_metadata": {
                                "order": 1,
                                "help": "sub-item string for option one",
                                "label": "Flexible Option One",
                                "field": "string"
                            }
                        }
                    },
                    "_metadata": {
                        "order": 9,
                        "help": "Help text for template one",
                        "label": "Template One",
                        "template": "testing-templates.html",
                        "field": "dict"
                    }
                },
                {
                    "schema": {
                        "dropdown": {
                            "type": "string",
                            "allowed": ["One", "Two"],
                            "_metadata": {
                                "order": 6,
                                "help": "Help text for dropdown example",
                                "label": "Dropdown Field",
                                "field": "dropdown",
                                "choices": ["One", "Two"]
                            }
                        }
                    },
                    "_metadata": {
                        "order": 9,
                        "help": "Help text for list example",
                        "label": "Template Two",
                        "template": "testing-templates-two.html",
                        "field": "dict"
                    }
                }
            ],
            "_metadata": {
                "order": 11,
                "help": "Help text for flexible content example",
                "label": "Flexible Content",
                "field": "flexible_content"
            }
        },
        "flexlist": {
            "type": "list",
            "schema": {
                "type": "dict",
                "anyof": [
                    {
                        "schema": {
                            "item": {
                                "type": "string",
                                "_metadata": {
                                    "order": 1,
                                    "help": "sub-item string for option one",
                                    "label": "Flexible Option One",
                                    "field": "string"
                                }
                            },
                            "template": {
                                "type":"string"
                            }
                        },
                        "_metadata": {
                            "order": 9,
                            "help": "Help text for template one",
                            "label": "Template One",
                            "template": "testing-templates.html",
                            "field": "dict"
                        }
                    },
                    {
                        "schema": {
                            "dropdown": {
                                "type": "string",
                                "allowed": ["One", "Two"],
                                "_metadata": {
                                    "order": 6,
                                    "help": "Help text for dropdown example",
                                    "label": "Dropdown Field",
                                    "field": "dropdown",
                                    "choices": ["One", "Two"]
                                }
                            },
                            "template": {
                                "type":"string"
                            }
                        },
                        "_metadata": {
                            "order": 9,
                            "help": "Help text for list example",
                            "label": "Template Two",
                            "template": "testing-templates-two.html",
                            "field": "dict"
                        }
                    }
                ],
                "_metadata": {
                    "order": 1,
                    "help": "Help text for flexible content example",
                    "label": "Flexible Content",
                    "field": "flexible_content"
                }
            },
            "_metadata": {
                "order": 12,
                "help": "help",
                "label": "List of Flexible Content Fields",
                "field": "list"
            }
        }
    },
    "embedded_fields": ['imagefield', 'objectid']
}
