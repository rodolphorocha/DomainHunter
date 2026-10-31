
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Dominio


class DominioAPITests(APITestCase):
    def setUp(self):
        User = get_user_model()

        self.usuario_a = User.objects.create_user(
            email='usuarioa@example.com',
            password='SenhaTeste123!',
            name='Usuário A',
        )

        self.usuario_b = User.objects.create_user(
            email='usuariob@example.com',
            password='SenhaTeste123!',
            name='Usuário B',
        )

        self.dominio_b = Dominio.objects.create(
            usuario=self.usuario_b,
            nome='exemplo',
            extensao='com.br',
        )

    
    def test_usuario_nao_lista_dominios_de_outro(self):
        self.client.force_authenticate(user=self.usuario_a)

        url = reverse('dominios-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(response.data['results'], [])


    def test_usuario_nao_exclui_dominio_de_outro(self):
        self.client.force_authenticate(user=self.usuario_a)

        url = reverse('dominios-detail', args=[self.dominio_b.id])
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.assertTrue(
            Dominio.objects.filter(pk=self.dominio_b.pk).exists()
        )

    def test_usuario_nao_visualiza_dominio_de_outro(self):
        self.client.force_authenticate(user=self.usuario_a)

        url = reverse('dominios-detail', args=[self.dominio_b.id])
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_usuario_nao_edita_dominio_de_outro(self):
        self.client.force_authenticate(user=self.usuario_a)

        url = reverse('dominios-detail', args=[self.dominio_b.id])

        response = self.client.patch(
            url,
            {'favorito': True},
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.dominio_b.refresh_from_db()
        self.assertFalse(self.dominio_b.favorito)
