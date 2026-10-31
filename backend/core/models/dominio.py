from django.conf import settings
from django.db import models



class Dominio(models.Model):

    class Extensao(models.TextChoices):
        COM = 'com', '.com'
        COM_BR = 'com.br', '.com.br'

    class Status(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        DISPONIVEL = 'disponivel', 'Aparentemente disponível'
        REGISTRADO = 'registrado', 'Registrado'
        INCONCLUSIVO = 'inconclusivo', 'Inconclusivo'

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dominios',
        )

    nome = models.CharField(max_length=63)

    extensao = models.CharField(
        max_length=6,
        choices=Extensao.choices,
        )

    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.PENDENTE,
        )

    favorito = models.BooleanField(default=False)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'nome', 'extensao'],
                name='unique_dominio_usuario',
            ),
        ]

    def __str__(self):
        return f'{self.nome}.{self.extensao}'