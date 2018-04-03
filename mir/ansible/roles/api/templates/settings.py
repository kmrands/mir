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
CREATE_ADMIN_APP = True
CREATE_IMAGE_API = True

# Auth
# -----------------
SECRET_KEY = os.getenv('MIR_SECRET_KEY', '{{secret_key}}')
AUTH_FIELD = 'owner'
OWNED_RESOURCES = ['accounts', 'person']
DEFAULT_ADMIN_USER = os.getenv('MIR_DEFAULT_ADMIN_USER', '{{default_admin_user}}')
DEFAULT_ADMIN_PW = os.getenv('MIR_DEFAULT_ADMIN_PW', '{{default_admin_pw}}')

# Cors
# -----------------
X_DOMAINS = '*'
X_HEADERS = ['X-Requested-With', 'Content-Type', 'If-match', 'Authorization']
X_ALLOW_CREDENTIALS = True

# Database
# -----------------
MONGO_HOST = os.getenv('MIR_MONGO_HOST', '{{mongo_host}}')
MONGO_PORT = os.getenv('MIR_MONGO_PORT', 27017)

# Get Database env vars if they exist
MONGO_USERNAME = os.getenv('MIR_MONGO_USERNAME', '{{mongodb_username}}')
MONGO_PASSWORD = os.getenv('MIR_MONGO_PASSWORD', '{{mongodb_pass}}')
MONGO_DBNAME = '{{mongo_dbname}}'

# Resource methods
# -----------------
RESOURCE_METHODS = ['GET', 'POST']
ITEM_METHODS = ['GET', 'PUT', 'PATCH', 'DELETE']
PUBLIC_METHODS = ['GET']
PUBLIC_ITEM_METHODS = ['GET']

# Media
# ------------------
RETURN_MEDIA_AS_BASE64_STRING = False
RETURN_MEDIA_AS_URL = True
