import requests
import csv
from bs4 import BeautifulSoup
import datetime


def page_search(soup):  # Функция находит и возвращает количество страниц
    pages = soup.find_all('a', class_='PaginationWidget__page')
    page_count = 0
    for i in pages:
        page_count = i.get('data-page')
    return page_count


def get_date_file():
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    date = []  # Список для добавления собранных данных

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/100.0.4896.127 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;'
                  'q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

    url = f'https://www.citilink.ru/catalog/televizory/?p='
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    name = soup.find('h1', class_='Heading Heading_level_1 Subcategory__title js--Subcategory__title').text.strip()
    page_count = page_search(soup)

    for j in range(1, int(page_count) + 1):
        url = f'https://www.citilink.ru'
        response = requests.get(url=f'https://www.citilink.ru/catalog/televizory/?p={j}', headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        parsing_products = soup.find_all('div', class_="product_data__gtm-js")

        for i in parsing_products:
            header_parsing = i.find('a', class_='ProductCardHorizontal__title')
            title = header_parsing.get('title')
            link = header_parsing.get('href')
            try:
                price = i.find('span', class_='ProductCardHorizontal__price_current-price').text.replace('\n', ''). \
                    replace(' ', '')
            except AttributeError:
                price = 'Товар отсутствует'

            date.append(
                [title, price, url + link]
            )

    with open(f'{name}_{cur_time}.csv', 'w') as file:
        writer = csv.writer(file)

        writer.writerow(
            [
                'Название',
                'Цена',
                'Ссылка',
            ]
        )

        writer.writerows(date)

    print(f'Файл {name}_{cur_time} записан')


def main():
    get_date_file()


if __name__ == '__main__':
    main()
