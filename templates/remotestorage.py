import boto3
import os
from rest_framework.exceptions import APIException
from django.conf import settings
import logging
# Get an instance of the logger
logger = logging.getLogger(__name__)


def generate_signed_url_from_bucket(s3_file_name):
    s3 = boto3.client('s3', 
                    endpoint_url=settings.BUCKET_ENDPOINT_URL,
                    aws_access_key_id=settings.BUCKET_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.BUCKET_SECRET_KEY,
                    config=boto3.session.Config(signature_version='s3v4'),
                    region_name=settings.BUCKET_REGION_NAME
                    )
    try:
        url = s3.generate_presigned_url('get_object',
                                        Params={'Bucket': settings.BUCKET_NAME,
                                                'Key': s3_file_name},
                                        ExpiresIn=int(settings.DURATION) * 1000
                                        )
        return url
    except Exception as e:
        logger.error('generateSignedUrlFromS3@Error')
        logger.error(e)
        return ""


def upload_file_to_bucket(file_path, s3_file_name, content_type):
    s3 = boto3.client('s3', 
                    endpoint_url=settings.BUCKET_ENDPOINT_URL,
                    aws_access_key_id=settings.BUCKET_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.BUCKET_SECRET_KEY,
                    region_name=settings.BUCKET_REGION_NAME
                    )
    extraArgs = {
            'ACL': 'public-read'
        }
    if content_type:
        extraArgs.update({
            'ContentType': content_type,
        })

    if content_type == None:
        content_type = ""
    try:
        s3.upload_file(
            file_path, 
            settings.BUCKET_NAME, 
            s3_file_name,
            ExtraArgs=extraArgs
            )
    except Exception as e:
        logger.error('uploadFileToS3@Error')
        logger.error(e)
        raise APIException(e)


def delete_file_from_bucket(s3_file_name):
    s3 = boto3.client('s3', 
                    endpoint_url=settings.BUCKET_ENDPOINT_URL,
                    aws_access_key_id=settings.BUCKET_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.BUCKET_SECRET_KEY,
                    region_name=settings.BUCKET_REGION_NAME
                    )
    try:
           s3.delete_object(
            Bucket=settings.BUCKET_NAME,
            Key=s3_file_name
        )
    except Exception as e:
        logger.error('deletFileS3@Error')
        logger.error(e)
        raise APIException(e)


def download_template_from_aws(s3_file_name, folder):
    s3 = boto3.client('s3', 
                    endpoint_url=settings.BUCKET_ENDPOINT_URL,
                    aws_access_key_id=settings.BUCKET_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.BUCKET_SECRET_KEY,
                    region_name=settings.BUCKET_REGION_NAME
                    )
    try:
        '''
        check if directory exist
        '''
        if not os.path.isdir(f"{settings.DOWNLOADED_ZIPPED_FILES_DIR}/{folder}"):
            os.makedirs(f"{settings.DOWNLOADED_ZIPPED_FILES_DIR}/{folder}")

        downloaded_template_path = f'{settings.DOWNLOADED_ZIPPED_FILES_DIR}{s3_file_name}'

        s3.download_file(
            Bucket=settings.BUCKET_NAME,
            Key=s3_file_name,
            Filename=downloaded_template_path
        )

        return downloaded_template_path

    except Exception as e:
        logger.error('downloadFileS3@Error')
        logger.error(e)
        raise APIException(e)
