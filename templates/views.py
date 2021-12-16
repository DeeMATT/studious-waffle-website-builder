from django.conf import settings
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
import mimetypes
import os
from datetime import datetime
from rest_framework.parsers import MultiPartParser
from .unzip import UnzipUploadedFile
from .validatezippedfilecontent import ValidateZippedFileContent
from .module import (
    generateLinearDictionaryOfTemplate,
    uploadFileToLocal,
    delete_dir,
    record_template
)
from .serializer import TemplateSerializer
from .remotestorage import upload_file_to_bucket


@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_processed_template(request):
    serialize_data = TemplateSerializer(data=request.data, context={'request': request})
    
    if serialize_data.is_valid():
        template = request.FILES.get('template_files')
        template_name = (str(datetime.now().timestamp()) + template.name).replace(" ", "")
        uploadFileToLocal(template, template_name)
        # extract content
        read_template_files = UnzipUploadedFile(template_name).read_zipped_file()

        ValidateZippedFileContent(read_template_files)
        
        extracted_files_dir = UnzipUploadedFile(template_name).extract_zipped_file()
        finalOutput =  generateLinearDictionaryOfTemplate(extracted_files_dir)

        # upload
        for filePath in finalOutput:
            mimetype = mimetypes.guess_type(filePath)[0]
            folder = f"{template_name}_/"
            if filePath.endswith('.css'):
                folderPath = folder + 'css/'
            elif filePath.endswith('.html'):
                folderPath = folder
            
            fileName = os.path.basename(filePath)
            s3FileName = f"{folderPath}{fileName}"
            upload_file_to_bucket(filePath, s3FileName, content_type=mimetype)
    
        # delete directory to free memory space
        delete_dir(extracted_files_dir)

        # generate url
        bucket_endpoint = settings.BUCKET_ENDPOINT_URL
        bucket_name = settings.BUCKET_NAME

        if not bucket_endpoint.endswith('/'):
            bucket_endpoint = bucket_endpoint + '/'
        
        template_url = f"{bucket_endpoint}{bucket_name}/{folder}index.html"

        # record template to db
        record_template(template_name, template_url)

        data = {
            "template_name": template_name,
            "template_url": template_url
        }
        
        return Response(data, status=status.HTTP_200_OK)

    else:
        return Response(serialize_data.errors, status=status.HTTP_400_BAD_REQUEST)
