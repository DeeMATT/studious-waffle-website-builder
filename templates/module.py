import time
from rest_framework.exceptions import ValidationError
import os
import json
import re
import shutil
from django.conf import settings
from os import listdir
from os.path import isfile, join, abspath
import logging
# Get an instance of the logger
logger = logging.getLogger(__name__)


def delete_downloaded_template(file):
    os.remove(file)


def validation_error_handler(message):
    raise ValidationError(message)


def generateLinearDictionaryOfTemplate(providedPath):
    if not providedPath.endswith("/"):
        providedPath = f"{providedPath}/"
    directoryContents = listdir(providedPath)
    filesToIgnore = ['dataspec.json']
    filesInThisDirectory = [
        f for f in directoryContents if isfile(join(providedPath, f))]
    foldersInThisDirectory = [
        f for f in directoryContents if not isfile(join(providedPath, f))]
    result = []
    for fileEntry in filesInThisDirectory:
        if not fileEntry in filesToIgnore:
            result.append(abspath(f"{providedPath}{fileEntry}"))
    for folderEntry in foldersInThisDirectory:
        result.extend(generateLinearDictionaryOfTemplate(
            f"{providedPath}{folderEntry}"))
    return result


def uploadFileToLocal(file, localPath):
    with open(localPath, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return True

def delete_dir(directory):
    try:
        shutil.rmtree(directory)
    except OSError as e:
        logger.error("Error: %s : %s" % (directory, e.strerror))
