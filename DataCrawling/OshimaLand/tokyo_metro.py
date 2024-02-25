from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time
import pickle

# TODO : 도쿄 지하철(도쿄 메트로) 수집


def load_page(url):
    driver = ChromeDriverManager().install()
    service = Service(excutable_path=driver)
    browser = webdriver.Chrome(service=service)
    browser.get(url)
    # browser.fullscreen_window()

    return browser


def get_content(browser):
    """
    도쿄 지하철 역 라인별 노선 정보 수집

    input : 웹브라우저 변수
    output : 라인별 상세노선 정보 
    author :장윤영
    updated date : 240224 


    """

    main_train = list()
    metro_link = {}

    metro_child = browser.find_elements(
        By.CSS_SELECTOR, "#v2_about > div.v2_wrapper > a"
    )

    for metro in metro_child:
        station = metro.find_element(By.CSS_SELECTOR, "p").text
        main_train.append(station)
        metro_link[station] = metro.get_attribute("href")
    line_detail = get_line_detail(browser, metro_link)

    return line_detail


def get_line_detail(browser, metro_link):
    """
    상세 노선 수집 함수 
    get_content() 내에서 실행 

    """

    line_detail_dict = {}

    for metro, link in metro_link.items():
        line_list = list()

        browser.get(link)
        time.sleep(3)

        line_detail = browser.find_elements(
            By.CSS_SELECTOR, "td.v2_cellStation > p > span > a"
        )

        for line in line_detail:
            line_list.append(line.text)

        line_detail_dict[metro] = line_list

    return line_detail_dict


    """
    딕셔너리 데이터 저장, 불러오는 함수 
    """

def save_dict(data, file_name):

    with open(file_name, 'wb') as f:
        pickle.dump(data, f)


def open_dict(file_name):
    with open(file_name, 'rb') as f:
        dictionary = pickle.load(f)
    return dictionary


url = "https://www.tokyometro.jp/en/subwaymap/index.html"
browser = load_page(url)
line_detail = get_content(browser)

save_dict(line_detail, 'DataCrawling/OshimaLand/line_detail.pkl')

