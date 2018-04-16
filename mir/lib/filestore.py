# -*- coding: utf-8 -*-

import time

import bucketstore
import cloudinary

from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from cloudinary.api import resources_by_tag, delete_resources

from eve.io.media import MediaStorage
from flask import current_app
"""
Amazon S3 Media Storage
"""


class AmazonMediaStorage(MediaStorage):
    """
    Subclass Eve's MediaStorage to use Amazon S3
    """

    def __init__(self, app=None):
        """
        :param app: the flask application (eve itself). This can be used by
        the class to access, amongst other things, the app.config object to
        retrieve class-specific settings.
        """
        # Get settings from App config
        aws_access_key_id = app.config['AWS_ACCESS_KEY_ID']
        aws_secret_access_key = app.config['AWS_SECRET_ACCESS_KEY']
        bucket_name = app.config['AWS_BUCKET']

        # Initialize our S3 Bucket
        bucketstore.login(aws_access_key_id, aws_secret_access_key)
        self.bucket = bucketstore.get(bucket_name, create=False)
        self.app = app

    def get(self, id_or_filename, resource=None):
        """ Opens the file given by name or unique id. Note that although the
        returned file is guaranteed to be a File object, it might actually be
        some subclass. Returns None if no file was found.
        """
        return self.bucket[id_or_filename] \
            if id_or_filename in self.bucket.list() else None

    def put(self, content, filename=None, content_type=None, resource=None):
        """ Saves a new file using the storage system, preferably with the name
        specified. If there already exists a file with this name name, the
        storage system may modify the filename as necessary to get a unique
        name. Depending on the storage system, a unique id or the actual name
        of the stored file will be returned. The content type argument is used
        to appropriately identify the file when it is retrieved.

        .. versionchanged:: 0.5
           Allow filename to be optional (#414).
        """
        if self.exists(filename):
            unique_filename = '%s-%s' % (str(int(time.time()) * 100), filename)
            try:
                item = self.bucket.key(unique_filename)
                item.set(content, content_type=content_type)
            except Exception as e:
                current_app.logger.error(e)
            return unique_filename
        else:
            try:
                item = self.bucket.key(filename)
                item.set(content, content_type=content_type)
            except Exception as e:
                current_app.logger.error(e)
            return filename

    def delete(self, id_or_filename, resource=None):
        """ Deletes the file referenced by name or unique id. If deletion is
        not supported on the target storage system this will raise
        NotImplementedError instead
        """
        if self.exists(id_or_filename):
            item = self.bucket.key(id_or_filename)
            item.delete()

    def exists(self, id_or_filename, resource=None):
        """ Returns True if a file referenced by the given name or unique id
        already exists in the storage system, or False if the name is available
        for a new file.
        """
        return id_or_filename in self.bucket.list()
