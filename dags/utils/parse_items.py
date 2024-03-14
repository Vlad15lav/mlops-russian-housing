import re
import time
import pandas as pd

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm


def test_request(browser, url, retry=3):
    """Тестовый запрос получения HTML страницы

    Args:
        browser: объект web driver selenium
        url: ссылка на страницу
        retry: количество попыток для запроса

    Returns:
        page_source: текстовая HTML страница
    """
    try:
        browser.get(url=url)
        time.sleep(3)
        return browser.page_source
    except Exception:
        time.sleep(3)

        if retry:
            return test_request(browser, url, retry=retry - 1)
        else:
            raise


def parse_date(text):
    """Преобразование текста информации о дате публикации

    Args:
        text: текстовая информация о дате публикации

    Returns:
        current_date: преобразованная дата побликации
    """
    split_text = text.split()
    hour, minute = map(int, split_text[-1].split(':'))
    current_date = datetime.now()
    current_date = current_date.replace(hour=hour, minute=minute,
                                        second=0, microsecond=0)

    if split_text[0] == 'вчера':
        current_date = current_date - timedelta(days=1)
    elif split_text[0] != 'сегодня':
        mask_month = {'января': 1, 'февраля': 2, 'марта': 3,
                      'апреля': 4, 'мая': 5, 'июня': 6, 'июля': 7,
                      'августа': 8, 'сентября': 9, 'октября': 10,
                      'ноября': 11, 'декабря': 12}
        day, month = int(split_text[0]), split_text[1]
        current_date = current_date.replace(day=day, month=mask_month[month])

    return current_date


def get_features_from_html(page_source, url):
    """Извлечение из HTML описания недвижимости

    Args:
        page_source: текстовая HTML страница
        url: ссылка на страницу

    Returns:
        link_list: список ссылок на недвижимость
    """
    soup = BeautifulSoup(page_source, "html.parser")
    params_html = soup.find_all("ul", class_="params-paramsList-_awNW")
    params_apartment, params_house = params_html
    params_apartment, params_house = params_apartment.text, params_house.text

    # Идентификатор недвижимости и город
    id_item = int(url.split('._')[-1])
    city_item = url.split('/')[3]

    # Время создания объявления
    date_item = soup.find('span', {"data-marker": "item-view/item-date"}).text
    date_item = parse_date(date_item[3:])

    # Регулярные выражения для поиска параметров квартиры
    re_rooms = re.compile(r'Количество комнат: \d+')\
        .search(params_apartment)
    re_rooms = int(re_rooms.group(0).split()[-1]) \
        if re_rooms else re_rooms

    re_square_total = re.compile(r'Общая площадь: (\d+.\d+|\d+)') \
        .search(params_apartment)
    re_square_total = float(re_square_total.group(0).split()[-1]) \
        if re_square_total else re_square_total

    re_square_cooking = re.compile(r'Площадь кухни: (\d+.\d+|\d+)') \
        .search(params_apartment)
    re_square_cooking = float(re_square_cooking.group(0).split()[-1]) \
        if re_square_cooking else re_square_cooking

    re_square_room = re.compile(r'Жилая площадь: (\d+.\d+|\d+)') \
        .search(params_apartment)
    re_square_room = float(re_square_room.group(0).split()[-1]) \
        if re_square_room else re_square_room

    re_floor = re.compile(r'Этаж: \d+') \
        .search(params_apartment)
    re_floor = int(re_floor.group(0).split()[-1]) \
        if re_floor else re_floor

    re_balcony = re.compile(r'Балкон или лоджия: [а-яё]+') \
        .search(params_apartment)
    re_balcony = re_balcony.group(0).split()[-1] \
        if re_balcony else re_balcony

    re_type_rooms = re.compile(r'Тип комнат: [а-яё]+') \
        .search(params_apartment)
    re_type_rooms = re_type_rooms.group(0).split()[-1] \
        if re_type_rooms else re_type_rooms

    re_repair = re.compile(r'Ремонт: [а-яё]+') \
        .search(params_apartment)
    re_repair = re_repair.group(0).split()[-1] \
        if re_repair else re_repair

    # Регулярные выражения для поиска параметров дома
    re_type = re.compile(r'Тип дома: [а-яё]+') \
        .search(params_house)
    re_type = re_type.group(0).split()[-1] \
        if re_type else re_type

    re_year_build = re.compile(r'Год постройки: \d+') \
        .search(params_house)
    re_year_build = int(re_year_build.group(0).split()[-1]) \
        if re_year_build else re_year_build

    re_max_floor = re.compile(r'Этажей в доме: \d+') \
        .search(params_house)
    re_max_floor = int(re_max_floor.group(0).split()[-1]) \
        if re_max_floor else re_max_floor

    re_elev_pass = re.compile(r'Пассажирский лифт: \d+') \
        .search(params_house)
    re_elev_pass = re_elev_pass.group(0).split()[-1] \
        if re_elev_pass else re_elev_pass

    re_elev_cargo = re.compile(r'Грузовой лифт: \d+') \
        .search(params_house)
    re_elev_cargo = re_elev_cargo.group(0).split()[-1] \
        if re_elev_cargo else re_elev_cargo

    # Регулярные выражение для объявления
    price = int(soup.find('span',
                          class_='styles-module-size_xxxl-A2qfi')['content'])

    return (
        id_item,
        date_item,
        city_item,
        re_rooms,
        re_square_total,
        re_square_cooking,
        re_square_room,
        re_floor,
        re_balcony,
        re_type_rooms,
        re_repair,
        re_type,
        re_year_build,
        re_max_floor,
        re_elev_pass,
        re_elev_cargo,
        price
    )


def parse_houses_data(url_filepath: str, output_filepath: str, **kwargs):
    """Парсинг ссылок на недвижимости со всех страниц

    Args:
        url_filepath: путь к файлу ссылок
        output_filepath: путь для записи файла
    """
    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) " +\
        "Gecko/20100101 Firefox/84.0"
    start_time = time.time()

    options = Options()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('log-level=3')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    rows = []
    error_counter = 0
    with webdriver.Remote('remote_chromedriver:4444/wd/hub',
                          options=options) as browser:

        browser.implicitly_wait(15)
        with open(url_filepath, 'r') as f:
            for url in tqdm(f.readlines()):
                try:
                    page_source = test_request(browser, url)
                    features = get_features_from_html(page_source, url)
                    rows.append(features)
                    error_counter = 0
                except Exception as e:
                    print('Browser Exception:', e)

                    time.sleep(10)
                    error_counter += 1
                    if error_counter > 5:
                        break

    df_data = pd.DataFrame(rows,
                           columns=['id', 'create_date', 'city_name',
                                    'room_count', 'total_square',
                                    'square_coock', 'square_rooms',
                                    'floor', 'loggia',
                                    'room_type', 'repair_type',
                                    'home_type', 'year_build',
                                    'max_floors', 'passanger_elevator',
                                    'cargo_elevator', 'price'])
    print(f'DataFrame shape: {df_data.shape}')
    df_data.to_csv(output_filepath, index=False)

    print('Done parsing houses href!')
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Execution time:', elapsed_time)


if __name__ == '__main__':
    parse_houses_data()
