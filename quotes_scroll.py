import requests
import pandas as pd

def run():
    quotes_list = extract_quotes_api()
    quotes_orderned = order_by_quotes_author(quotes_list)
    save_csv(quotes_orderned)

def order_by_quotes_author(quotes_list):
    quotes_list.sort(key=lambda x: x['Author'])
    print('Ordenado por autor.')
    return quotes_list

def save_csv(quotes_list):
    file_name = 'quotes_scroll.csv'
    df = pd.DataFrame(quotes_list)
    df.to_csv(file_name, index=False)
    print('Arquivo criado com sucesso!')

def extract_quotes_api():
    page = 0
    quotes_list=[]
    url = 'https://quotes.toscrape.com/api/quotes?page={}'
    url_goodreads = 'https://www.goodreads.com'
    while(True):
        page += 1
        try:
            response = requests.get(url.format(page))
            quotes_json = response.json()
            if not quotes_json['has_next']:
                print('Fim da pagina.')
                return quotes_list
            for quotes in quotes_json['quotes']:
                text = quotes['text']
                author = quotes['author']['name']
                tags = quotes['tags']
                link_author_goodreads = url_goodreads + quotes['author']['goodreads_link']
                info_quotes = {
                    'Author': author,
                    'Text': text,
                    'Tags': tags,
                    'Goodreads_link': link_author_goodreads
                }
                quotes_list.append(info_quotes)
                print('dados da página {} capturados. '.format(page))
        except Exception as e:
            print(e)
            print('erro ao capturar dados da página {}'.format(page))

if __name__ == '__main__':
    run()