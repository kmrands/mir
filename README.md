# Mir Framework

A framework for creating complex, highly-customizable REST APIs and their management dashboards with minimal effort.

Built on top of [Eve](http://python-eve.org/).

---

## Installation

Mir can be installed using [pip](https://pip.pypa.io/en/stable/installing/). The python package includes the framework's core files and a CLI tool used for creating and scaffolding projects, running development and production servers, and deploying your project.

```bash
pip install mir
```

*Mir requires a running [MongoDB](https://docs.mongodb.com/manual/installation/) instance.*

---

## Starting a Project

Like Eve, Mir is simple.

```bash
# initialize a project
mir init my_new_project

# navigate to your project directory
cd my_new_project

# Create a new endpoint
mir model -n new_endpoint

# start a dev server at http://localhost:8080
mir dev

curl http://localhost:8080/new_endpoint
```

---

## Features

* Mir creates highly customizable REST APIs using simple, readable configuration files as an alternative to manual CRUD programming. You configure settings and validation for your database resources and get a REST API for free.

* Automatically creates flexible, fully-featured web-based Admin UIs to manage your API based on the settings and validation specified in your resource configuration files.

* Includes fully customizable token-based authentication out of the box. Control access per resource, per user, and/or per role via the application's configuration files.

* Includes document versioning for all resources.

* Includes media storage for files, videos, and images. Mir also implements an API for manipulating images on-the-fly via query string parameters, modeled after the [Cloudinary](https://cloudinary.com/) service.

* Implements interfaces and APIs for creating custom application routes, request hooks, etc.

* Provides code APIs for customizing much of the core functionality, including media/file storage and authentication.

---

## Development

To get started developing Mir, first clone the repo and install it as a python package in development mode:

```bash
git clone https://github.com/spbrien/mir.git
pip install -e ./mir
```

* The core application (which imports/registers all project-specific code and other python modules) is in `mir/mir.py`
* The CLI tool is in `mir/cli.py`
* The source code for the Admin UI is in `admin/src`

### Working on the API core files

In a separate directory, scaffold out and run a new Mir project:

```bash
mir init test_project
cd test_project
mir dev
```

Once you have a running Mir instance, you can update core files and see your changes in the running instance. Due to the way Mir dynamically imports python modules from project-specific code, many changes require manually restarting the development server:

```bash
ctrl + c
mir dev
```

### Working on the Admin UI

In a separate testing directory, scaffold out and run a new Mir project:

```bash
mir init test_project
cd test_project
mir dev
```

In your main Mir directory, change to the admin application folder and start a dev server:

```bash
cd admin
npm run dev
```

This starts a frontend development server for the Admin Vue application at http://localhost:8081

To build your changes into the running mir instance, run `npm run build` and restart the mir dev server from the testing directory. For the Admin UI, build files should be committed to the Mir package repo.

---

For full documentation, visit the [Python Mir](http://python-mir.org) website.
