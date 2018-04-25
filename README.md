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

For full documentation, visit the [Python Mir](http://python-mir.org) website.
