from django.urls import path
from .views import upload_processed_template

urlpatterns = [
    path("/upload-template/", upload_processed_template)
]
