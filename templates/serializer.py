from rest_framework import serializers


class TemplateSerializer(serializers.Serializer):
    template_files = serializers.FileField(required=True, write_only=True)
    template_name = serializers.CharField(read_only=True)
    template_url = serializers.CharField(read_only=True)
