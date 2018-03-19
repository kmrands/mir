# Mir Framework

Mir is a REST API and CMS framework, built using [Eve](http://python-eve.org/). It was created to further reduce the effort involved in creating, managing and deploying REST APIs. While Eve already simplifies the creation of complex REST APIs, Mir takes the process one step further:

* Provides a set of default configurations and implementation for features that Eve does not provide: Authentication, external Media Storage, etc
* Provides tooling for scaffolding model configurations
* Provides tooling and a framework for simplified implementation of application routes and hooks
* Provides a fully featured and automatically generated Admin Dashboard for the created API

## Dependencies

* Homebrew
* Python 2.7
* pip
* A running MongoDB instance

## Installation

If [Homebrew](https://brew.sh/) is not installed, install it:

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Using homebrew, install Python and pip:

```
brew install python
```

Add the following to your `.bash_profile`:

```
export PATH="/usr/local/opt/python/libexec/bin:$PATH";
source ~/.bash_profile
```

Ensure the installation worked:

```
python --version && pip --version
```

Install Mir:

```
pip install git+git://github.com/spbrien/mir.git#egg=mir
```

Start a new project:

```
mir init new-project
```
