
import requests
from bs4 import BeautifulSoup
import pandas as pd


class Quotes:
    def __init__(self, user, password):
        self.url_base = 'https://quotes.toscrape.com'
        self.url_login = "https://quotes.toscrape.com/login"
        self.user = user
        self.password = password
        self.session = requests.Session()
        self.list_quotes = []
        self.response = None

    def eval_login(self):
        if self.response.status_code == 200:
            print('Login realizado com sucesso!')
            return True
        else:
            print('Login falhou!')
            return False

    def login(self):
        data = {
            'username': self.user,
            'password': self.password,
        }
        self.response = self.session.post(self.url_login, data=data)
        status_login = self.eval_login()
        return status_login

    def run(self):
        status_login = self.login()
        if status_login:
            self.response = self.session.get(self.url_base)
            self.capturar_dados()
            self.order_quotes_by_key('Author')
            self.save_csv()
            print('Arquivo criado com sucesso!')
        else:
            print('erro ao fazer login')

    def order_quotes_by_key(self, key):
        self.list_quotes.sort(key=lambda x: x[key])

    def save_csv(self):
        file_name = 'quotes_with_class.csv'
        df = pd.DataFrame(self.list_quotes)
        df.to_csv(file_name, index=False)

    def next_page(self, soup):
        try:
            url_next_page = soup.find(
                'li', {"class": "next"}).find('a').get('href')
            self.response = self.session.get(f"{self.url_base}{url_next_page}")
            self.capturar_dados()
        except AttributeError:
            print('Chegou na ultima pagina. ')

    def capturar_dados(self):
        soup = BeautifulSoup(self.response.text, "html.parser")
        quotes = soup.findAll('div', {"class": "quote"})
        for quote in quotes:
            phrase = quote.find('span', {"class": "text"}).get_text(strip=True)
            author = quote.find(
                'small', {"class": "author"}).get_text(strip=True)
            soup_tags = quote.find('div', {"class": "tags"}).findAll('a')
            tags = [tag.getText() for tag in soup_tags]
            tags = ', '.join(tags)
            info_quotes = {
                'Author': author,
                'Text': phrase,
                'Tags': tags,
            }
            self.list_quotes.append(info_quotes)
        self.next_page(soup)


if __name__ == '__main__':
    quotes = Quotes('wesley', 'wesleypassword')
    quotes.run()
