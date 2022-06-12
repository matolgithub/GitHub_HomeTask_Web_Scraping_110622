import requests as re
from bs4 import BeautifulSoup as bs
from pprint import pprint

def get_html_page():
    site_link = 'https://habr.com'
    add_link = '/ru/all/'
    url = site_link + add_link
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
    return soup, url, site_link

def get_articles():
    soup, url, site_link = get_html_page()
    count_articles = 0
    articles = soup.find_all(class_='tm-articles-list__item')
    articles_list = []
    print('*' * 150, 'Данные по статьям: ')
    for article in articles:
        count_articles += 1
        date_publ = article.find(class_="tm-article-snippet__datetime-published").find('time').attrs['title']
        title = article.find(class_="tm-article-snippet__title tm-article-snippet__title_h2").text
        article_link = article.find(class_="tm-article-snippet__title-link").attrs['href']
        hub = article.find(class_="tm-article-snippet__hubs").text
        try:
            article_text = article.find(class_="article-formatted-body article-formatted-body article-formatted-body_version-2").text
        except AttributeError:
            article_text = article.find(class_="article-formatted-body article-formatted-body article-formatted-body_version-1").text
        clean_article_text = article_text.replace('\n\n', '').replace('\r\n', ''). replace('\n', '').replace('\xa0', '')
        print(f'Статья №{count_articles}: Дата/время: {date_publ} -- Заголовок: {title} -- Ссылка: {site_link}'
                  f'{article_link} -- Текст статьи: {clean_article_text} -- Хабы: {hub}')
        articles_list.append([count_articles, date_publ, title, site_link + article_link, clean_article_text, hub])

    return articles_list

def select_articles():
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']
    articles_list = get_articles()
    result_list = []
    for word in KEYWORDS:
        for item_article in articles_list:
            if word in item_article[2] or word in item_article[4] or word in item_article[5]:
                result_list.append(item_article)
    print('*' * 150, 'Выборка статей: ')
    pprint(result_list)
    print('*' * 70, 'РЕЗУЛЬТИРУЮЩАЯ ВЫБОРКА: ', '*' * 70)
    for item_list in result_list:
        print(f'{item_list[1]} - {item_list[2]} - {item_list[3]}.')
    return result_list

if __name__ == '__main__':
    select_articles()