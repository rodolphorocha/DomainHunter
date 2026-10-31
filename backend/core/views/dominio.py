from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.models import Dominio
from core.serializers.dominio import DominioSerializer


class DominioViewSet(viewsets.ModelViewSet):
    serializer_class = DominioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Dominio.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)