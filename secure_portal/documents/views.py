from rest_framework import viewsets
from accounts.permissions import DocumentPermission
from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [DocumentPermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)