# Creating Custom Routes

To add custom routes to your API, you can use the `route` command:

```
mir route
```


## Default Route Definition

This will prompt you for a `name`, then create your route file.

The code generated in `./routes/<name>.py` should look something like the following:

```
from flask import Blueprint, request, jsonify, render_template

<name> = Blueprint('test', __name__)


@<name>.route('/')
def index():
    status_code = 200
    data = {
        'route': 'working'
    }

    return jsonify(data), status_code
```

In order for Mir to import your custom route correctly, the variable that holds the blueprint object must be the same as the name of your file.


## Reusing Routes Across Projects

As with resources and hooks, routes can be installed from raw github URLs:

```
mir route --url https://raw.githubusercontent.com/path/to/your/route.py
```

## References

* [Flask Blueprints](http://flask.pocoo.org/docs/0.12/blueprints/) _(note that all blueprints added according to the above conventions are added automatically to the application by Mir)_
