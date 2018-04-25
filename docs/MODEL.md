# Creating Resources

To add resources or endpoints to your API, you can use the `model` command:

```bash
mir model
```

## Default Model Definition

The above command will display an interactive prompt asking for a name for your model. Model names should only contain letters and underscores. Once a name is provided, the mir cli tool will create a new file at `./models/<name>.py` containing a base schema definition:

```python
model = {
    "schema": {
        "slug": {
            "type": "string",
            "regex": "^[a-z0-9]+(?:-[a-z0-9]+)*$",
            "required": True,
            "unique": True,
            "minlength": 0,
            "maxlength": 400,
            "_metadata": {
                "order": 1,
                "help": "May only contain alpha-numeric characters and dashes",
                "label": "Resource URL String",
                "field": "slug"
            }
        },
        "published": {
            "type": "boolean",
            "_metadata": {
                "order": 2,
                "help": "Should this item appear publicly as a published item?",
                "label": "Published",
                "field": "checkbox"
            }
        },
    },
    "additional_lookup": {
        "url": "regex('[\\w-]+')",
        "field": "slug"
    },
    "datasource": {
        "default_sort": [("_created", -1)]
    }
}
```

The [model](http://python-eve.org/config.html#domain-configuration)/[schema](http://python-eve.org/config.html#schema-definition) definitions for Mir follow the same structure and produce the same functionality as in [Eve](http://python-eve.org/config.html#domain-configuration). The only difference is the inclusion of the `_metadata` field for each key of the schema definition. This field is used to generate the Admin Dashboard and requires the fields `order, help, label, and field`. Further, the `field` property is used to generate the proper input html and must be one of the following values:

* checkbox
* checklist
* dict
* dropdown
* flexible_content
* imagefield
* list
* objectid
* password
* radio
* richtext
* simplelist
* slug
* string


## Example Model Definition

To see an example of how each of these properties are used, and what the type of interface they generate, scaffold out an example resource:

```bash
mir model --example
```

This command will produce an extensive example model in the file `models/example.py`, containing both Eve settings for different types of resources and the specific `_metadata` content that must be set for each type:

```python
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
    }
}
```

## Reusing Models Across Projects

Models can be reused across projects with the help of git raw URLs or gists. The mir framework will install a model directly from a URL. Let's use the default Mir `media` model as an example:

```
mir model --url https://raw.githubusercontent.com/spbrien/mir/master/mir/lib/default_models/media.py
```

Again, you will be prompted for a name. Your new file, located at `./models/<name>.py` will contain the text found at the raw [github url](https://raw.githubusercontent.com/spbrien/mir/master/mir/lib/default_models/media.py):

```
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
            "allowed": ["Image", "Audio"]
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
```

## References

* [Eve Domain Configuration](http://python-eve.org/config.html#domain-configuration)
* [Eve Schema Definitions](http://python-eve.org/config.html#schema-definition)
