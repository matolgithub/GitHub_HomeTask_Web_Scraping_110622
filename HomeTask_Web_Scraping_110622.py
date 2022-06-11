import requests as re
from bs4 import BeautifulSoup as bs
from pprint import pprint

# определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# Ваш код
def get_html_page():
    url = 'https://habr.com/ru/all/'
    HEADERS = {
        'accept-language': 'ru-RU,ru;q=0.9',
        'cookie': 'yandexuid=7517158921651275583; i=BfXMTmCzHSgXtAltGVouXdmLDy62Y88MRkbxDsxkvQcwZY2ZxGj3YY/QmyMKfqCv6VnD5UtWB+PFH36oUnMsrd7yVQk=; yuidss=7517158921651275583; ymex=1970333463.yrts.1654973463',
        'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36'
    }
    res_get = re.get(url, headers=HEADERS)
    soup = bs(res_get.text, 'html.parser')
    # pprint(soup)
    return soup

def get_articles():
    soup = get_html_page()
    articles = soup.find(class_='tm-articles-list').find_all(class_='tm-articles-list__item')
    # pprint(articles)
    dates_publ = soup.find_all(class_="tm-article-snippet__datetime-published")
    # pprint(dates_publ)
    titles = soup.find_all(class_="tm-article-snippet__title tm-article-snippet__title_h2")
    pprint(titles)
    # for post in posts:
    #     post_id = post.parent.attrs.get('id')
    #     # если идентификатор не найден, это что-то странное, пропускаем
    #     if not post_id:
    #         continue
    #     post_id = int(post_id.split('_')[-1])
    #     print('post', post_id)



if __name__ == '__main__':
    # get_html_page()
    get_articles()