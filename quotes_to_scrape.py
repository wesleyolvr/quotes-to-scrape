
import requests
from bs4 import BeautifulSoup
import pandas as pd


def avalia_login(resposta_login):
    resposta = {}
    soup = BeautifulSoup(resposta_login.text, "html.parser")
    if resposta_login.status_code == 200:
        resposta['mensagem'] = 'ok'
        resposta['status_code'] = '200'
    else:
        resposta['mensagem'] = 'erro_login'
        resposta['status_code'] = '400'
    return resposta


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
    resultado = avalia_login(resposta_login)
    resultado["session"] = session
    return resultado


def avanca_pagina(soup, sessao,lista_citacoes):
    url = 'https://quotes.toscrape.com'
    try:
        url_prox_pagina = soup.find(
            'li', {"class": "next"}).find('a').get('href')
        prox_pagina = url + url_prox_pagina
        captura_dados_e_printa(sessao=sessao,
                               url=prox_pagina,
                               lista_citacoes=lista_citacoes)
    except AttributeError:
        print('Chegou na ultima pagina. ')


def captura_dados_e_printa(sessao, url, lista_citacoes):
    """recebe um response da pagina 'quotes.toscrape' e printa as informações como:
        'Citacao', 'Autor', 'Tags'

    Args:
        response ([Response]): response da pagina de 'quotes.toscrape'
    """
    response = sessao.get(url)
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
        lista_citacoes.append(dados)

    avanca_pagina(
        soup = soup,
        sessao = sessao,
        lista_citacoes=lista_citacoes
    )
    return lista_citacoes


def run():
    url='https://quotes.toscrape.com/'
    user='wesley'
    password='12345'
    resposta_login=login(
        username = user, password = password, url = url)
    sessao=resposta_login['session']
    if resposta_login['mensagem'] == 'ok':
        return captura_dados_e_printa(sessao = sessao,
                               url = url,
                               lista_citacoes = [])
    else:
        logout(sessao)
        raise Exception('Erro de login. tente novamente')


if __name__ == '__main__':
    dados = run()
    df = pd.DataFrame(dados)
    print(df)
    file_name = 'citacoes.csv'
    df.to_csv(file_name, sep=',')
    
