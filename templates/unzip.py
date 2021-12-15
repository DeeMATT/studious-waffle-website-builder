from zipfile import ZipFile, is_zipfile
from .module import validation_error_handler, delete_downloaded_template
import json
import time,os
from django.conf import settings

class UnzipUploadedFile:
    zipped_file = ''

    def __init__(self, uploaded_file):
        self.file = uploaded_file
        self.validate_file_is_zip()

    def validate_file_is_zip(self):
        if is_zipfile(self.file):
            return self
        else:
            return validation_error_handler({'file_error': 'Template files must be in a zipped format'})

    def read_zipped_file(self):
        with ZipFile(self.file, 'r') as zipped_file:
            self.zipped_file = zipped_file
            return zipped_file.namelist()

    def extract_zipped_file(self):
        '''
        check if directory exist
        '''
        if not os.path.isdir(settings.EXTRACTED_FILES_DIR):
            os.mkdir(settings.EXTRACTED_FILES_DIR)
        
        file_path = f'{settings.EXTRACTED_FILES_DIR}/{time.time()}'

        with ZipFile(self.file) as zipped_file:
            zipped_file.extractall(file_path)
        '''
        delete downloaded file
        '''
        delete_downloaded_template(self.file)
        return file_path



