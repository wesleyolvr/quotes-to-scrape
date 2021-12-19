
import requests
import json
from bs4 import BeautifulSoup


def captura_dados_e_printa(response):
    """recebe um response da pagina 'quotes.toscrape' e printa as informações como:
        'Citacao', 'Autor', 'Tags'

    Args:
        response ([Response]): response da pagina de 'quotes.toscrape'
    """
    soup = BeautifulSoup(response.text,"html.parser")
    citacoes = soup.findAll('div',{"class":"quote"})
    for citacao in citacoes:
        data = {}
        frase = citacao.find('span',{"class":"text"}).get_text(strip=True)
        author = citacao.find('small',{"class":"author"}).get_text(strip=True)
        soup_tags = citacao.find('div',{"class":"tags"}).findAll('a')
        tags = [tag.getText() for tag in soup_tags]
        data = {
            'citacao': frase,
            'autor' : author,
            'tags' : tags,
        }
        print(json.dumps(data,indent=4,ensure_ascii=False))
    try:
        url_next_page = soup.find('li',{"class":"next"}).find('a').get('href')
    except:
        return
    next_page = url_base + url_next_page
    response = requests.get(next_page)
    captura_dados_e_printa(response)

url_base = 'https://quotes.toscrape.com/'
response = requests.get(url_base)
captura_dados_e_printa(response)