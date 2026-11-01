
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


RDAP_URLS = {
    'com': 'https://rdap.verisign.com/com/v1/domain/',
    'com.br': 'https://rdap.registro.br/domain/',
}



def consultar_dominio(nome, extensao):
    if extensao not in RDAP_URLS:
        raise ValueError('Extensão não suportada.')

    dominio = f'{nome}.{extensao}'
    url = RDAP_URLS[extensao] + dominio

    request = Request(
        url,
        headers={'Accept': 'application/rdap+json'},
    )

    try:
        with urlopen(request, timeout=10) as response:
            dados = json.load(response)

            if (
                dados.get('objectClassName') == 'domain'
                and dados.get('ldhName', '').lower() == dominio
            ):
                return 'registrado'

            return 'inconclusivo'

    except HTTPError as erro:
        if erro.code == 404:
            return 'disponivel'

        return 'inconclusivo'

    except (URLError, TimeoutError, ValueError):
        return 'inconclusivo'
