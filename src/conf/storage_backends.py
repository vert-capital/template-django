from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.AWS_STATIC_LOCATION
    file_overwrite = True
    object_parameters = {
        "CacheControl": "max-age=86400",
    }

    def _get_security_token(self):
        return None


class PublicMediaStorage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = False
    object_parameters = {
        "CacheControl": "max-age=86400",
    }

    def _get_security_token(self):
        return None


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    file_overwrite = False
    custom_domain = False
    object_parameters = {
        "CacheControl": "max-age=86400",
    }

    def _get_security_token(self):
        return None
