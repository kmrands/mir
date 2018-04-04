# Mir Framework

Mir is a REST API and CMS framework built on top of [Eve](http://python-eve.org/). It was created to further reduce the effort involved in creating, managing and deploying REST APIs. While Eve already simplifies the creation of complex REST APIs, Mir takes the process one step further:

* Provides a set of default configurations and implementation for features that Eve does not provide: Authentication, external Media Storage, etc
* Provides tooling for scaffolding model configurations
* Provides tooling for scaffolding application routes and hooks
* Simplifies the implementation of models, custom routes and request hooks
* Provides a fully-featured and automatically-generated Admin Dashboard for the created API

## Dependencies

* Homebrew
* Python 2.7
* pip
* A running MongoDB instance

## Installation

If [Homebrew](https://brew.sh/) is not installed, install it:

```bash
# Make sure xcode is installed
xcode-select --install

# Install homebrew
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Using homebrew, install Mongodb, Python and pip:

```bash
# MongoDB -- Be sure to follow any post-install instructions
# output by Homebrew
brew install mongodb
brew services start mongodb

# Python and pip
brew install python
```

Add the following to your `.bash_profile`:

```bash
export PATH="/usr/local/opt/python/libexec/bin:$PATH";
```

Run the profile script

```bash
source ~/.bash_profile
```

Ensure the installation worked:

```bash
python --version && pip --version
```

Install Mir:

```bash
pip install git+git://github.com/spbrien/mir.git#egg=mir
```

## References

* [Installing Python](http://docs.python-guide.org/en/latest/starting/install/osx/)
