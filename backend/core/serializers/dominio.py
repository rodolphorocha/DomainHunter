
import re

from rest_framework import serializers

from core.models import Dominio


class DominioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dominio
        fields = [
            'id',
            'nome',
            'extensao',
            'status',
            'favorito',
            'criado_em',
        ]
        read_only_fields = [
            'id',
            'status',
            'criado_em',
        ]

    def validate_nome(self, value):
        nome = value.strip().lower()

        if not re.fullmatch(
            r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?',
            nome,
        ):
            raise serializers.ValidationError(
                'Informe um nome de domínio válido.'
            )

        return nome

    def validate(self, attrs):
        usuario = self.context['request'].user

        nome = attrs.get(
            'nome',
            self.instance.nome if self.instance else None,
        )

        extensao = attrs.get(
            'extensao',
            self.instance.extensao if self.instance else None,
        )

        dominios = Dominio.objects.filter(
            usuario=usuario,
            nome=nome,
            extensao=extensao,
        )

        if self.instance:
            dominios = dominios.exclude(pk=self.instance.pk)

        if dominios.exists():
            raise serializers.ValidationError(
                'Você já possui um domínio com este nome e extensão.'
            )

        return attrs