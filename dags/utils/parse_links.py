import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

URL = "https://www.avito.ru"
REGION_LIST = ('moskva', 'sankt-peterburg', 'kazan')


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
        time.sleep(1)
        return browser.page_source
    except Exception:
        time.sleep(3)

        if retry:
            return test_request(browser, url, retry=retry - 1)
        else:
            raise


def get_links_from_html(page_source):
    """Извлечение из HTML разметки ссылки на недвижимость

    Args:
        page_source: текстовая HTML страница

    Returns:
        link_list: список ссылок на недвижимость
    """
    soup = BeautifulSoup(page_source, "html.parser")
    links = soup.find_all("div", class_="iva-item-title-py3i_")
    link_list = []
    for link in links:
        link_list.append(URL + link.find('a')['href'])

    return link_list


def get_houses_links(output_filepath: str,
                     pages: int = 100,
                     **kwargs):
    """Парсинг ссылок на недвижимость со всех страниц

    Args:
        output_filepath: путь для записи файла
        pages: количество рассматриваемых страниц
    """
    start_time = time.time()

    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--log-level=3')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    link_list = []
    with webdriver.Remote('remote_chromedriver:4444/wd/hub',
                          options=options) as browser:
        for region in REGION_LIST:
            for page in tqdm(range(1, pages + 1)):
                cur_url = f"https://www.avito.ru/{region}/kvartiry" + \
                    "/prodam/vtorichka-ASgBAgICAkSSA8YQ5geMUg" + \
                    f"?p={page}&s=104"
                page_source = test_request(browser, cur_url)
                link_list += get_links_from_html(page_source)

    print(f'Total links: {len(link_list)}')
    with open(output_filepath, 'w') as fp:
        for item in link_list:
            fp.write("%s\n" % item)

    print('Done parsing houses href!')
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Execution time:', elapsed_time)


if __name__ == '__main__':
    get_houses_links()
