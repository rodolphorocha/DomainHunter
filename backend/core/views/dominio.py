from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.models import Dominio
from core.serializers.dominio import DominioSerializer

from rest_framework.decorators import action
from rest_framework.response import Response

from core.services.rdap import consultar_dominio


class DominioViewSet(viewsets.ModelViewSet):
    serializer_class = DominioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Dominio.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['get'])  
    def consultar(self, request):
         nome = request.query_params.get('nome')
         extensao = request.query_params.get('extensao')

         if not nome or not extensao:
            return Response(
                {'erro': 'Informe o nome e a extensão.'},
                status=400,
            )

    
    