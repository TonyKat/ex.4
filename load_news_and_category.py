'''
Разработка классификатора новостей
Нужно:
выбрать какой-либо новостной ресурс, где к новостям привязаны категории или метки
(например http://lenta.ru, http://fontanka.ru, http://gazeta.ru)
загрузить новости по некоторому набору (5-10) категорий за пару лет
обучить классификатор на эти новостях
продемонстрировать его работу, разработав простеший web-интерфейс (вариант - telegram-бот),
куда пользователь вводит текст новости и на выходе получает наиболее вероятную категорию.
В качестве фреймворка проще всего взять Flask (см. примеры) .
'''

# -*- coding: utf-8 -*
import time
import requests
from multiprocessing.dummy import Pool as ThreadPool
from functools import reduce
from bs4 import BeautifulSoup
from tqdm import tqdm


def html_page(url):
    request = session.get(url)
    return request.text


def write_to_file(news,category):
    with open('file_news1.txt', 'w', encoding='utf-8') as output_file:
        for i in range(len(news)):
            output_file.write(news[i])
        
    with open('file_category1.txt', 'w', encoding='utf-8') as output_file:
        for i in range(len(category)):
            output_file.write(category[i])


def get_urls_years_and_days():
    urls_years = []
    # получить ссылки на календари годов
    for i in range(5):
        urls_years.append('http://www.fontanka.ru/fontanka/arc/' + str(2012-i) + '/all.html')
    # получить ссылки на дни календаря
    url_year_days = []
    for i in range(len(urls_years)):
        data = html_page(urls_years[i])
        soup = BeautifulSoup(data, 'html5lib')
        path_to_days = soup.find_all('td', {'class': 'dom'})
        days = []
        for j in range(len(path_to_days)):
            if path_to_days[j].a is not None:
                days.append(url_first_page + path_to_days[j].a.get('href'))
        url_year_days.append(days)
    return url_year_days


def get_news(url):
    data = html_page(url)
    soup = BeautifulSoup(data, 'html5lib')
    path_news = soup.find_all('div', {'class': 'calendar-item-title'})
    news = []
    for i in range(len(path_news)):
        news.append(path_news[i].a.text)
    return news


def get_category(url):
    data = html_page(url)
    soup = BeautifulSoup(data, 'html5lib')
    path_category = soup.find_all('div', {'class': 'calendar-item-category'})
    category = []
    for i in range(len(path_category)):
        category.append(path_category[i].a.text)
    return category


def get_news_and_category(url_year_days):
    news_all = []
    category_all = []
    pool = ThreadPool(10)
    for k in tqdm(range(len(url_year_days))):
        news = pool.map(get_news, url_year_days[k])
        category = pool.map(get_category, url_year_days[k])
        news = reduce(lambda x, y: x + y, news)
        category = reduce(lambda x, y: x + y, category)
        news_all.append(news)
        category_all.append(category)
    news_all = reduce(lambda x, y: x + y, news_all)
    category_all = reduce(lambda x, y: x + y, category_all)
    return news_all,category_all


if __name__ == '__main__':
    time_begin = time.time()
    session = requests.Session()
    session.headers.update({
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    })
    url_first_page = 'http://www.fontanka.ru'
    url_year_days = get_urls_years_and_days()
    news, category = get_news_and_category(url_year_days)
    write_to_file(news,category)
    print('Время исполнения программы: ', time.time() - time_begin)
    exit()