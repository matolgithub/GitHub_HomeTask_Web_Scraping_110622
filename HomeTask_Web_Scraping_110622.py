import requests as re
from bs4 import BeautifulSoup as bs
from pprint import pprint


def input_menu():
    while True:
        input_item = input("Приветствуем! Введите (1 - поиск по preview, 2 - поиск по всему тексту статей): ")
        if input_item == "1":
            select_articles()
            break
        elif input_item == "2":
            selfrom_allarticle()
            break
        else:
            print("Ваш ввод не понятен! Попробуйте снова!")

def get_html_page(site_link='https://habr.com', url='https://habr.com/ru/all/'):
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
    return result_list, articles_list, KEYWORDS

def selfrom_allarticle():
    result_list_preview, articles_list, KEYWORDS = select_articles()
    result_list_total = []
    count_articles = 0
    for item in articles_list:
        count_articles += 1
        print("/" *  150, f'Полная статья №{count_articles}:')
        soup, url, site_link = get_html_page(site_link='https://habr.com', url=item[3])
        try:
            article_text = soup.find(class_="article-formatted-body article-formatted-body article-formatted-body_version-2").text
        except AttributeError:
            article_text = soup.find(class_="article-formatted-body article-formatted-body article-formatted-body_version-1").text
        clean_article_text = article_text.replace('\n\n', '').replace('\r\n', ''). replace('\n', '').replace('\xa0', '')
        tags_article_list = soup.find_all(class_="tm-separated-list__item")
        for tag_article in tags_article_list:
            clean_article_text += tag_article.text.strip() + ' '
        print(clean_article_text)
        for word in KEYWORDS:
            if word in clean_article_text:
                result_list_total.append([item[1], item[2], item[3]])
    result_list_preview = [i[1:4] for i in result_list_preview]
    link_article = [i[2] for i in result_list_preview]
    for article in result_list_total:
        if article not in result_list_preview:
            result_list_preview.append(article)
    print('\n', '*' * 70, 'РЕЗУЛЬТАТ ВЕБ-СКРАПИНГА ПОЛНОГО ТЕКСТА СТАТЕЙ: ', '*' * 70)
    print(f'Ранее были найдены {len(link_article)} статьи(ей):', *link_article)
    print(f'Теперь, при скрапинге всего текста найдено {len(result_list_preview)} статьи(ей):')
    for item_art in result_list_preview:
        print(f'{item_art[0]} - {item_art[1]} - {item_art[2]}')
    return result_list_preview


if __name__ == '__main__':
    input_menu()