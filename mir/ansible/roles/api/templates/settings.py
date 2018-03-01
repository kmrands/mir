import os

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
OPLOG = True
OPLOG_NAME = 'log'
OPLOG_ENDPOINT = 'log'
OPLOG_AUDIT = True
PAGINATION_LIMIT = 5000
PAGINATION_DEFAULT = 25
HATEOAS = True
VERSIONING = True

# Auth
# -----------------
SECRET_KEY = os.getenv('MIR_SECRET_KEY', 'secret')
AUTH_FIELD = 'owner'
DEFAULT_ADMIN_USER = os.getenv('MIR_DEFAULT_ADMIN_USER', 'admin')
DEFAULT_ADMIN_PW = os.getenv('MIR_DEFAULT_ADMIN_PW', 'test')

# Cors
# -----------------
X_DOMAINS = '*'
X_HEADERS = ['X-Requested-With', 'Content-Type', 'If-match', 'Authorization']
X_ALLOW_CREDENTIALS = True

# Database
# -----------------
MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017

# Get Database env vars if they exist
MONGO_USERNAME = os.getenv('MIR_MONGO_USERNAME', None)
MONGO_PASSWORD = os.getenv('MIR_MONGO_PASSWORD', None)
MONGO_DBNAME = '{{project_name}}'

# Resource methods
# -----------------
RESOURCE_METHODS = ['GET', 'POST']
ITEM_METHODS = ['GET', 'PUT', 'PATCH', 'DELETE']
PUBLIC_METHODS = ['GET']
PUBLIC_ITEM_METHODS = ['GET']
