from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from googletrans import Translator

import requests
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

def save_dict(data, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump(data, f)


def open_dict(file_name):
    with open(file_name, 'rb') as f:
        dictionary = pickle.load(f)
    return dictionary


def papago_translate(text, client_id, client_seceret):
    """
    PAPAGO API 이용 영어 노선도 한국어로 번역 

    input : taget(지하철 역),  client_id, client_seceret
    output : 한국어 노선도 
    author :장윤영
    updated date : 240225 


    """
    client_id = client_id
    client_secret = client_seceret

    a='error'
    b = "error"
    if text.encode().isalpha():
        text_lng = 'en'
        target_lng = 'ko'
    else:
        text_lng = 'ko'
        target_lng = 'en'
    data = {'text' : text,
            'source' : text_lng,
            'target': target_lng}

    url = "https://openapi.naver.com/v1/papago/n2mt"

    header = {"X-Naver-Client-Id":client_id,
            "X-Naver-Client-Secret":client_secret}

    response = requests.post(url, headers=header, data= data)
    rescode = response.status_code

    if(rescode==200):
        t_data = response.json()
        return response.json()['message']['result']['translatedText']
    else:
        print("Error Code:" , rescode)
        return 0
    
def translate_kr(data):
    for key, value in data.items():
        tokyo_kr_list = list(map(lambda line: papago_translate(line.replace('-', ''), client_id, client_seceret),value))
        data[key] = tokyo_kr_list

    save_dict(data, 'DataCrawling/OshimaLand/line_detail_kr.pkl')


url = "https://www.tokyometro.jp/en/subwaymap/index.html"
browser = load_page(url)
line_detail = get_content(browser)

file_name = 'DataCrawling/OshimaLand/line_detail_kr.pkl'
translate_kr(line_detail, file_name)


