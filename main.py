import config

from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import datetime
import random

# ad some flag, i
CHECK_DB_FLAG = False

# код для прокси

def ip_proxy_adreses():
    # бесплатный серис с проски парсим с него прокси, не работает.... Пидр...
    proxy_page = requests.get('https://free-proxy-list.net/')
    proxy_soup = BeautifulSoup(proxy_page.text, 'html.parser')
    proxy_card = proxy_soup.find('table')
    proxy_card_proxys = proxy_card.find_all('tr')
    all_proxis = []
    for i in proxy_card_proxys:
        temp_proxy = []
        for idx, val in enumerate(i.find_all('td')):
            if idx == 2:
                break
            temp_proxy.append(val.get_text())
        if len(temp_proxy) < 2:
            continue
        else:
            full_proxy = temp_proxy[0] + ":" + temp_proxy[1]
            all_proxis.append(full_proxy)
    return all_proxis


ip_addresses = config.proxy


# тут у нас код отвечающий за скрапинг странцы, и сохранения как текста
def get_web_page_from_url(ad_url):
    # переходим на страниwу и парсим все данные со страницы
    proxy_index = random.randint(0, len(ip_addresses) - 1)
    print(proxy_index)
    proxy = {"http": ip_addresses[proxy_index], "https": ip_addresses[proxy_index]}
    print(ad_url)
    page = requests.get(ad_url)
    # page = requests.get(ad_url, proxies=proxy)
    return page


def get_html_text_from_page(get_page):
    # закидываем сюда, то что прислал get_page_fromad_url
    ad_page = BeautifulSoup(get_page.text, 'html.parser')
    return ad_page


# дата фрейм для хранения данных
df = pd.DataFrame(columns=['main_url', 'card_url', 'title', 'adress', 'metro_st', 'ap_info', 'text_sub', 'apart_feat',
                           'ad_apart_feat', 'rent_pr', 'info_rent_pr', 'pay_info', 'phone', 'owner_id',
                           'curr_dat', 'upl_dt', 'statis'])


def write_to_csv(df):
    """
    get data frame and ad it to csv file
    :param df:
    """
    with open('my_csv.csv', 'a') as f:
        df.to_csv(f)

# Не все работает
def create_url(page_number):
    # создает URL страницы
    return "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&p={}&region=1&room1=1&room9=1&type=4".format(
        str(page_number))


def get_navigation_last_num_element(element_number, url):
    # возвращает последний элемент нав меню внизу страницы
    new_page = requests.get(url)
    soup = BeautifulSoup(new_page.text, 'html.parser')
    return soup.find_all(class_="_93444fe79c--list-itemLink--3o7_6")[element_number].get_text()


def count_number_of_category_pages(url):
    # считает кол-во страниц в выбранной категории, запускается на странице
    while True:
        pages_menu_last__numeric_element = get_navigation_last_num_element(-1, url)
        if pages_menu_last__numeric_element.isdigit():
            # проверяет какой последний элемент, если тот цифра то значит это индекс
            # последней страницы
            return pages_menu_last__numeric_element
        else:
            # в ином случае вытаскивает предпослежний элемент и использует в качестве
            # индекса для генерация новой страницы на которой проверяется последний
            # элемент
            # может быть 1
            pages_menu_last__numeric_element = get_navigation_last_num_element(-2, url)
            url = create_url(pages_menu_last__numeric_element)
            inner_soup = BeautifulSoup(requests.get(url).text, 'html.parser')


# функция по генерированию URl с карточками объявлений
DEAL_TYPE = 'rent'  # sale - покупка, напишите в кавычках sale если хотите
# посомтреть покупку (пока не работает функция)
PAGE_COUNT = 54  # надо ввести кол-во страниц сцществующих, на циане


def url_list_generator(length):
    url_list = []
    page_number = 0
    url = create_url(page_number)
    for i in range(1, length):
        url = create_url(page_number)
        url_list.append(url)
        page_number += 1
    return url_list


def get_ads_from_categorial_page(soup):
    # извлекает карточки
    cards = soup.find_all(class_='_93444fe79c--card--_yguQ')
    return cards


# Берем ЮРЛ карточки
def get_ads_url(card):
    card_url = card.find('a', class_="c6e8ba5398--header--1fV2A", href=True)['href']
    return card_url


# надо сделать функции для каждой
def get_title(card_page):
    # Наименование объявления тег H1
    if card_page.find('h1', class_="a10a3f92e9--title--2Widg"):
        return card_page.find('h1', class_="a10a3f92e9--title--2Widg").get_text()
    return "NAN"


def get_adress(card_page):
    if card_page.find('address', class_="a10a3f92e9--address--140Ec"):
        return card_page.find('address', class_="a10a3f92e9--address--140Ec").get_text()
    return "NAN"


def get_metro_station(card_page):
    # список станций
    if card_page.find_all('li', class_="a10a3f92e9--underground--kONgx"):
        metro_station = card_page.find_all('li', class_="a10a3f92e9--underground--kONgx")
        list_of_stations = []
        for i in metro_station:
            list_of_stations.append(i.get_text())
        return list_of_stations
    return "NAN"


def apartments_info(card_page):
    if card_page.find_all('div', class_="a10a3f92e9--info-text--2uhvD"):
        apartments_info = card_page.find_all('div', class_="a10a3f92e9--info-text--2uhvD")
        all_apartmenrs_info = []
        for q in apartments_info:
            all_apartmenrs_info.append(q.get_text())
        return all_apartmenrs_info
    return "NAN"


def text_subscription(card_page):
    if card_page.find('p', class_="a10a3f92e9--description-text--1_Lup"):
        return card_page.find('p', class_="a10a3f92e9--description-text--1_Lup").get_text()
    return "NAN"


def aparments_features(card_page):
    # дополнительная инфа, есть ли стиралк, микроволновка и т.д.
    if card_page.find('ul', class_="a10a3f92e9--container--L-EIV"):
        additional_appartments_info = card_page.find('ul', class_="a10a3f92e9--container--L-EIV")
        appartments_features = []
        for i in additional_appartments_info:
            appartments_features.append(i.get_text())
        return appartments_features
    return "NAN"


def additional_appartments_feature(card_page):
    # еще дополнительные фичи, тут вроде площадь жидая совмещенный ли санузел и т.д.
    if card_page.find_all(class_="a10a3f92e9--value--3Ftu5"):
        additional_features = []
        for i in card_page.find_all(class_="a10a3f92e9--value--3Ftu5"):
            additional_features.append(i.get_text())
        return additional_features
    return "NAN"


def get_rent_price(card_page):
    # стоимость аренды
    if card_page.find(class_="a10a3f92e9--price_value--1iPpd"):
        return card_page.find(class_="a10a3f92e9--price_value--1iPpd").get_text().replace(u'\xa0', ' ')
    return "NAN"


def get_information_for_rent_price(card_page):
    # информация по стоимости аренды
    if card_page.find(class_="a10a3f92e9--more_price_rent---5hwY"):
        return card_page.find(class_="a10a3f92e9--more_price_rent---5hwY").get_text().replace(u'\xa0', ' ')
    return "NAN"


def get_additional_payment_info(card_page):
    # дополнительная информация по оплате
    if card_page.find(class_="a10a3f92e9--description--2xRVn"):
        return card_page.find(class_="a10a3f92e9--description--2xRVn").get_text().replace(u'\xa0', ' ').split(",")
    return "NAN"


def get_phone_numbers(card_page):
    # номера телефонов!!
    if card_page.find(class_="a10a3f92e9--container--35iPF"):
        return card_page.find(class_="a10a3f92e9--container--35iPF").get_text().replace('Показать телефон', '').replace(
            'Написать сообщение', '').split('+')
    return "NAN"


def get_owner_id(card_page):
    # название агентства
    if card_page.find('h2', class_="a10a3f92e9--title--2gUWg"):
        return card_page.find('h2', class_="a10a3f92e9--title--2gUWg").get_text()
    elif card_page.find(class_="a10a3f92e9--id--LA2Ew"):
        return card_page.find(class_="a10a3f92e9--id--LA2Ew").get_text()
    return "NAN"


def get_current_date():
    # возвращает сегодняшнюю дату и время
    import datetime
    return str(datetime.datetime.today())


def get_upload_datetime(card_page):
    # Время и дата загрузки
    if card_page.find(class_="a10a3f92e9--container--3nJ0d"):
        return card_page.find(class_="a10a3f92e9--container--3nJ0d").get_text()
    return "NAN"


def get_statistics(card_page):
    # Берет статистику за сегодня
    if card_page.find(class_="a10a3f92e9--link--1t8n1 a10a3f92e9--link--2mJJk"):
        return card_page.find(class_="a10a3f92e9--link--1t8n1 a10a3f92e9--link--2mJJk").get_text()
    return "Nan"


def create_full_data_list(card_page, main_page_url, card_url):
    # Берет инфу из всех функций и запихивает внутрь листа, чтобы потом в DF заебенить
    full_data = []
    full_data.append(main_page_url)
    full_data.append(card_url)
    full_data.append(get_title(card_page))
    full_data.append(get_adress(card_page))
    full_data.append(get_metro_station(card_page))
    full_data.append(apartments_info(card_page))
    full_data.append(text_subscription(card_page))
    full_data.append(aparments_features(card_page))
    full_data.append(additional_appartments_feature(card_page))
    full_data.append(get_rent_price(card_page))
    full_data.append(get_information_for_rent_price(card_page))
    full_data.append(get_additional_payment_info(card_page))
    full_data.append(get_phone_numbers(card_page))
    full_data.append(get_owner_id(card_page))
    full_data.append(get_current_date())
    full_data.append(get_upload_datetime(card_page))
    full_data.append(get_statistics(card_page))
    return full_data


def check_rows_in_csv():
    """
    In this method we check value in csv file, did they exist or not
    we need this for correct scraping data
    :return: index of the row in csv file
    """
    df = pd.read_csv('my_csv.csv')
    last_row: int = df.shape[0]
    while True:
        if df.loc[last_row, 'title'] == type(str):
            return last_row
        else:
            last_row = last_row - 1






# парсим пробегаемся по сгенерированным страницам, собираем карточки, переходим на карточку, собираем
# данне с карточки сохраняем в DF добавляем к большому DF

page_list = url_list_generator(54)
for i in page_list:
    # у нас есть все юрл страничек, теперь для каждой страницы нам надо извлечь список карточек
    # надо каким то образом проверять, на
    # еще нужно добавить тут фигню уотора

    web_page = get_web_page_from_url(i)
    print(web_page)
    soup = get_html_text_from_page(web_page)
    print(soup)
    ads_url = get_ads_from_categorial_page(soup)  # функция с url стрниц
    # если ЮРЛ страниц на месте, то надо провер добавить функцию проверки, наличия записей
    last_row = check_rows_in_csv()
    for idx, val in enumerate(ads_url):
        # добавим сна, чтобы не блочил сервак
        time.sleep(1)
        ad_url = get_ads_url(val)
        web_ad_page = get_web_page_from_url(ad_url)
        ad_page = get_html_text_from_page(web_page)
        index = last_row + idx
        df.loc[index] = create_full_data_list(ad_page, i, ad_url)
        write_to_csv(df)
        print(index, ad_url)
