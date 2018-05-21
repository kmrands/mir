# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# THIS FILE IS ONLY PARTIALLY USED IN APPLICATIONS DEPLOYED WITH THE MIR CLI
# YOUR CHANGES TO CERTAIN SETTINGS WILL HAVE NO AFFECT ON YOUR DEPLOYED APP
# Documentation coming soon
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os

# Optional AWS Storage
# from mir.lib.filestore import AmazonMediaStorage


# -----------------------------------
# Settings
# -----------------------------------

# Global
# -----------------
DEBUG = True
URL_PREFIX = 'api'
API_VERSION = 'v1'
XML = False
UPSERT_ON_PUT = False
SCHEMA_ENDPOINT = 'info'
IF_MATCH = True
EMBEDDING = True
JSON_SORT_KEYS = True
CACHE_CONTROL = 'no-cache, must-revalidate'
CACHE_EXPIRES = 0
OPLOG = False
# OPLOG_NAME = 'log'
# OPLOG_ENDPOINT = 'log'
# OPLOG_AUDIT = True
# OPLOG_METHODS = ["DELETE", "POST", "PATCH", "PUT"]
# OPLOG_CHANGE_METHODS = ["DELETE", "POST", "PATCH", "PUT"]
# OPLOG_RETURN_EXTRA_FIELD = True
PAGINATION_LIMIT = 5000
PAGINATION_DEFAULT = 25
HATEOAS = True
VERSIONING = True
MULTIPART_FORM_FIELDS_AS_JSON = True
CREATE_ADMIN_APP = True
CREATE_IMAGE_API = True

# Auth
# -----------------
SECRET_KEY = 'secret'
AUTH_FIELD = 'owner'
OWNED_RESOURCES = ['accounts', 'person']
DEFAULT_ADMIN_USER = 'admin'
DEFAULT_ADMIN_PW = 'test'

# Cors
# -----------------
X_DOMAINS = '*'
X_HEADERS = ['X-Requested-With', 'Content-Type', 'If-match', 'Authorization']
X_ALLOW_CREDENTIALS = True

# Database
# -----------------
MONGO_HOST = os.environ.get(MIR_MONGO_HOST, '127.0.0.1')
MONGO_PORT = os.environ.get(MIR_MONGO_PORT, 27017)

# Get Database env vars if they exist
MONGO_USERNAME = None
MONGO_PASSWORD = None
MONGO_DBNAME = '{{data.name}}'

# Resource methods
# -----------------
RESOURCE_METHODS = ['GET', 'POST']
ITEM_METHODS = ['GET', 'PUT', 'PATCH', 'DELETE']
PUBLIC_METHODS = ['GET']
PUBLIC_ITEM_METHODS = ['GET']

# Media
# ------------------
RETURN_MEDIA_AS_BASE64_STRING = True
EXTENDED_MEDIA_INFO = ['content_type', 'name', 'length']
RETURN_MEDIA_AS_URL = False

# AWS Storage
# ------------------
# AWS_ACCESS_KEY_ID = ''
# AWS_SECRET_ACCESS_KEY = ''
# AWS_BUCKET = ''
# MEDIA = AmazonMediaStorage
