import os
import sys
import subprocess
import importlib
import urllib.request
import time
import pickle


# TODO : 도쿄 지하철(도쿄 메트로) 수집

client_id = 'CLIRNT_ID'
client_secret = 'CLIENT_SECRET'


def install(package, upgrade=True):
    """
    Python 패키지를 설치하거나 업그레이드합니다.
    
    매개변수:
    - package (str): 설치 또는 업그레이드할 패키지의 이름.
    - upgrade (bool): 이미 설치된 패키지를 업그레이드할지 여부. 기본값은 True입니다.
    
        작성자: 장윤영
        업데이트 날짜: 240302
    """
    try:
        # 이미 설치된 패키지인지 확인
        importlib.import_module(package)
        print(f"{package} 패키지는 이미 설치되어 있습니다. 업그레이드 여부에 따라 패키지를 업그레이드하거나 넘어갑니다.")
    except ModuleNotFoundError:
        try:
            # pip 명령어 구성
            command = [sys.executable, '-m', 'pip', 'install', package]
            if upgrade:
                command.append('--upgrade')
            
            # pip 명령어 실행
            subprocess.check_call(command)
            
            # 설치된 패키지 임포트 시도
            importlib.import_module(package)
            print(f"{package} 패키지가 성공적으로 설치되었습니다.")
        except subprocess.CalledProcessError:
            print(f"패키지 설치 중 오류 발생: {package}. 패키지 이름과 인터넷 연결을 확인해주세요.")
        except Exception as e:
            print(f"예상치 못한 오류가 발생했습니다: {e}")


install("selenium")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def load_page(url):
    """
    페이지 로드
    author : 장윤영
    updated date : 240224

    updated by : 이지은
    updated date : 240226

    """
    browser = webdriver.Chrome()
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
    with open(file_name, "wb") as f:
        pickle.dump(data, f)


def open_dict(file_name):
    with open(file_name, "rb") as f:
        dictionary = pickle.load(f)
    return dictionary


def papago_translate(text, client_id, client_secret):
    """
    PAPAGO API 이용 영어 노선도 한국어로 번역

    input : taget(지하철 역),  client_id, client_seceret
    output : 한국어 노선도
    author :장윤영
    updated date : 240302

    ERROR : urllib.error.HTTPError: HTTP Error 404: Not Found

    """

    text_lng = "en"
    target_lng = "ko"

    data = f"source={text_lng}&target={target_lng}&text=" + text

    url = "https://openapi.naver.com/v1/papago/n2mt"


    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)


def translate_kr(data, file_name):
    for key, value in data.items():
        tokyo_kr_list = list(
            map(
                lambda line: papago_translate(
                    line.replace("-", ""), client_id, client_secret
                ),
                value,
            )
        )
        data[key] = tokyo_kr_list

    save_dict(data, file_name)

if __name__ == "__main__":
    install("requests")

    url = "https://www.tokyometro.jp/en/subwaymap/index.html"
    browser = load_page(url)
    line_detail = get_content(browser)

    file_name = "DataCrawling/data/line_detail_kr.pkl"
    translate_kr(line_detail, file_name)