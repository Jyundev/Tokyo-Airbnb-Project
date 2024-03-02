import pickle
from tqdm import tqdm
import pandas as pd 
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# TODO : 도쿄 지하철역 기준 부동산 사건/사고 데이터 수집 

def open_dict(file_name):
    with open(file_name, "rb") as f:
        dictionary = pickle.load(f)
    return dictionary

def load_page(url):
    """
    페이지 로드
    author : 장윤영
    updated date : 240302
    
    """
        
    browser = webdriver.Chrome()
    browser.get(url)
    browser.fullscreen_window()

    return browser


def get_fire(driver, tokyo_oshima, station):
    """
    부동산 사건/사고 데이터 수집 

    input : 웹브라우저 변수, 도쿄 부동산 사건/사고 데이터 리스트, 검색 지역 
    output : 도쿄 부동산 사건/사고 데이터 리스트
    author : 장윤영
    updated date : 240302
    
    """    

    fire_objects = driver.find_elements(By.CSS_SELECTOR, ".map-fire")
    print(len(fire_objects))
    original_window_handle = driver.current_window_handle 

    for fire in fire_objects:
        try:
            if fire.is_displayed():
                actions = ActionChains(driver)                 
                driver.execute_script("arguments[0].click();", fire)
                actions.move_to_element(fire).click().perform()

                time.sleep(5)
                # WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.property-info-date > span')))
                info_date = driver.find_element(By.CSS_SELECTOR, 'li.property-info-date > span').text
                info_address = driver.find_element(By.CSS_SELECTOR, 'li.property-info-address').text
                info_content = driver.find_element(By.CSS_SELECTOR, 'div.popup-property-info > section > ul > li:nth-child(3)').text

                info = {
                    'district': station,
                    'date': info_date,
                    'address': info_address,
                    'content': info_content
                }

                tokyo_oshima.append(info)

                time.sleep(3)

                if len(driver.window_handles) > 1:
                    driver.switch_to.window(original_window_handle)

        except Exception as e:
            print("Error:", e)
            continue

    return tokyo_oshima


def search_metro_fire(tokyo_metro, driver, file_name):
    """
    지하철역 기준 부동산 사건/사고 데이터 검색  

    input : 도쿄 지하철 역, 웹브라우저 변수, 도쿄 부동산 사건/사고 데이터 저장 파일 이름 
    output : 도쿄 부동산 사건/사고 데이터
    author : 장윤영
    updated date : 240302
    
    """    
        
    tokyo_oshima = list()

    menu = driver.find_element(By.CSS_SELECTOR, "#header-menu-button")
    menu.click()

    time.sleep(2)

    # English version
    eng_btn = driver.find_element(By.CSS_SELECTOR, "#menu-container > div > section:nth-child(4)")
    eng_btn.click()

    search_tab = driver.find_element(By.CSS_SELECTOR, '#geocoder-text')
    search_btn = driver.find_element(By.CSS_SELECTOR, "#geocoder-button")

    for key, value in tqdm(tokyo_metro.items()):
        print(key)
        for metro in value:
            search_tab.clear()
            search_tab.send_keys(metro + ' station')

            search_btn.click()  # 수정: send_keys 대신 click 사용

            time.sleep(3)

            tokyo_oshima = get_fire(driver, tokyo_oshima, metro)
            print(tokyo_oshima)

    
    df = pd.DataFrame(tokyo_oshima)
    df.to_csv(file_name, index=False, encoding='utf-8')


    return tokyo_oshima

if __name__ == "__main__":
    file_name = 'DataCrawling/data/line_detail.pkl'
    tokyo_metro = open_dict(file_name)

    url = 'https://www.oshimaland.co.jp/'
    driver = load_page(url)

    file_name = 'DataCrawling/data/oshima_metro.csv'
    tokyo_oshima_dict = search_metro_fire(tokyo_metro, driver, file_name)
    tokyo_oshima_dict