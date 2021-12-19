
import requests
import json
from bs4 import BeautifulSoup


def logout(session):
    url_logout = "https://quotes.toscrape.com/logout"
    session.get(url_logout)

def login(url, username, password):
    session = requests.Session()
    url_login = url + "login"
    response_login = session.get(url_login)
    soup = BeautifulSoup(response_login.text, "html.parser")
    csrf_token = soup.find(
        'input', {"name": "csrf_token", "value": True})['value']
    data = {
        "csrf_token": csrf_token,
        "username": username,
        "password": password
    }
    resposta_login = session.post(url=url_login, data=data)
    if resposta_login.status_code == 200:
        return resposta_login, session, 'ok'
    else:
        return resposta_login, session, 'erro_login'


def avanca_pagina(soup, sessao):
    url = 'https://quotes.toscrape.com'
    try:
        url_prox_pagina = soup.find(
            'li', {"class": "next"}).find('a').get('href')
        prox_pagina = url + url_prox_pagina
        response_next_pagina = sessao.get(prox_pagina)
        captura_dados_e_printa(response_next_pagina,sessao)
    except AttributeError:
        print('Chegou na ultima pagina. ')


def captura_dados_e_printa(response, sessao):
    """recebe um response da pagina 'quotes.toscrape' e printa as informações como:
        'Citacao', 'Autor', 'Tags'

    Args:
        response ([Response]): response da pagina de 'quotes.toscrape'
    """
    soup = BeautifulSoup(response.text, "html.parser")
    citacoes = soup.findAll('div', {"class": "quote"})
    for citacao in citacoes:
        dados = {}
        frase = citacao.find('span', {"class": "text"}).get_text(strip=True)
        author = citacao.find(
            'small', {"class": "author"}).get_text(strip=True)
        soup_tags = citacao.find('div', {"class": "tags"}).findAll('a')
        tags = [tag.getText() for tag in soup_tags]
        dados = {
            'citacao': frase,
            'autor': author,
            'tags': tags,
        }
        print(json.dumps(dados,
                         indent=4,
                         ensure_ascii=False)
              )

    avanca_pagina(
        soup=soup,
        sessao=sessao
    )


def run():
    url = 'https://quotes.toscrape.com/'
    user = 'wesley'
    password = '12345'
    s = requests.Session()
    response_logado, sessao, status_login = login(
        username=user, password=password, url=url)
    if status_login == 'ok':
        response_logado = sessao.get(url)
        captura_dados_e_printa(response=response_logado,
                               sessao=sessao)
    else:
        logout(sessao)
        raise Exception('Erro de login. tente novamente')


if __name__ == '__main__':
    run()
