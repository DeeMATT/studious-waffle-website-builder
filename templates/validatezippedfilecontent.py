from zipfile import ZipFile
from .module import validation_error_handler


class ValidateZippedFileContent:
    def __init__(self, template_files):

        self.template_files = template_files
        if isinstance(self.template_files, list):
            _template_files = list()
            for x in self.template_files:
                if '/' in x:
                    x = x.split('/')[0]
                if x not in _template_files:
                    _template_files.append(x)

            if 'index.html' not in _template_files:
                raise validation_error_handler({'file_error': 'Please the template must have an index.html file'})
            if 'css' not in _template_files:
                raise validation_error_handler({'file_error': 'Please the template must have a css folder'})
