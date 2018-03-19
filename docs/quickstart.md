# Initializing A Project

The `init` command sets up the necessary files and folder structure for a Mir project.

```
mir init new-project
```

## Application Structure

The above command will produce the following folder structure:

```
└── new-project
    ├── AUTHORS.md
    ├── CONTRIBUTING.md
    ├── README.md
    ├── Vagrantfile
    ├── __init__.py
    ├── client
    ├── hooks
    │   └── __init__.py
    ├── inventories
    │   ├── production
    │   │   ├── group_vars
    │   │   │   └── all
    │   │   └── hosts
    │   └── staging
    │       ├── group_vars
    │       │   └── all
    │       └── hosts
    ├── models
    │   └── __init__.py
    ├── requirements.txt
    ├── routes
    │   └── __init__.py
    ├── settings.py
    ├── static
    └── templates
        └── index.html
```


## Running a Development Server

You can now run a Mir development server, listening at http://localhost:8080

```
cd new-project
mir dev
```

Visiting the above link will return JSON specifying a 404 error. By default, Mir provides all API endpoints at `/api/v1/<endpoint>`. Try visiting http://localhost:8080/api/v1/info. You should see JSON output representing all of the models' schema in your application. For now, there should only be a `media` schema shown.


## Application Settings

Take a look at `./settings.py` to see the default project settings. Most of these will require updating for a production application. For development, you only need to specify the connection information for your running MongoDB instance. There is no need to specify a DOMAIN setting as it is built automatically by the framework.

## References

* [Eve Settings](http://python-eve.org/config.html#global-configuration)
