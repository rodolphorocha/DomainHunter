
import json
from io import BytesIO
from unittest.mock import patch

from django.test import SimpleTestCase

from core.services.rdap import consultar_dominio


class RDAPTests(SimpleTestCase):
    def test_extensao_nao_suportada(self):
        with self.assertRaises(ValueError):
            consultar_dominio('exemplo', 'xyz')

    @patch('core.services.rdap.urlopen')
    def test_dominio_registrado(self, mock_urlopen):
        resposta = {
            'objectClassName': 'domain',
            'ldhName': 'google.com',
        }

        conteudo = json.dumps(resposta).encode('utf-8')

        mock_urlopen.return_value.__enter__.return_value = BytesIO(
            conteudo
        )

        resultado = consultar_dominio('google', 'com')

        self.assertEqual(resultado, 'registrado')
