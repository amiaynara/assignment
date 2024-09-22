"""DRF File serializer"""

from rest_framework import serializers

# App imports
from app.models import File


class FileSerializer(serializers.Serializer):
    """File serializer class"""

    class Meta:
        model = File
        fields = []