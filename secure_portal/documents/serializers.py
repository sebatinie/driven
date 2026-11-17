from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Document
        fields = ["id", "title", "content", "owner", "created_at"]