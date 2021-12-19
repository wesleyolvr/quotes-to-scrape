import requests
from bs4 import BeautifulSoup



def desafio(response):
    soup = BeautifulSoup(response.text,"html.parser")
    linhas = soup.findAll('div',{"class":"quote"})
    for linha in linhas:
        print('Citacao:', linha.find('span',{"class":"text"}).getText())
        print('Autor:', linha.find('small',{"class":"author"}).getText())
        soup_tags = linha.find('div',{"class":"tags"}).findAll('a')
        tags = [tag.getText() for tag in soup_tags]
        print('Tags:', *tags,end='\n\n')
    try:
        url_next_page = soup.find('li',{"class":"next"}).find('a').get('href')
    except:
        return
    next_page = url_base + url_next_page
    response = requests.get(next_page)
    desafio(response)

url_base = 'https://quotes.toscrape.com/'
response = requests.get(url_base)
desafio(response)
print('fim de papo!')
