from bs4 import BeautifulSoup
import urllib.request as req
from tqdm import tqdm_notebook
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# TODO : 도쿄 네이버 여행 상품 숙소 정보 수집


def get_optionurl():
    """
    체크인, 체크아웃, 성인(만 18세 이상), 어린이(만 18세 미만) 인원 수에 따라 숙소 정보 변동
    :return:
    """
    checkin_year, checkin_month, checkin_day = input(
        "Enter the check-in date (YYYY MM DD format): "
    ).split()
    checkout_year, checkout_month, checkout_day = input(
        "Enter the check-out date (YYYY MM DD format): "
    ).split()
    adultnum = input("Enter the number of adults: ")
    childnum = input("Enter the number of children: ")
    child_age_list = []
    baseurl = "https://hotels.naver.com/"

    if int(childnum) > 0:
        for _ in range(int(childnum)):
            child_age_list.append(
                input("Enter the age of child (below 18 years old): ")
            )
        optionurl = (
            f"{baseurl}list?placeFileName=place%3ATokyo&&adultCnt={(adultnum)}"
            + "&childAges="
            + "%2C".join(child_age_list)
            + f"&checkIn={(checkin_year)}-{(checkin_month)}-{(checkin_day)}&"
            f"checkOut={(checkout_year)}-{(checkout_month)}-{(checkout_day)}&includeTax=false&sortField=popularityKR&sortDirection=descending"
        )
    else:
        optionurl = (
            f"{baseurl}list?placeFileName=place%3ATokyo&&adultCnt={adultnum}&checkIn={(checkin_year)}-{(checkin_month)}-{(checkin_day)}&"
            + "checkOut={(checkout_year)}-{(checkout_month)}-{(checkout_day)}&includeTax=false&sortField=popularityKR&sortDirection=descending"
        )
    print(f"Go to option Link : {optionurl}")
    return optionurl


def get_detailurl(optionurl):
    """
    숙소 상세 정보 url
    :param optionurl:
    :return:
    """
    driver = webdriver.Chrome()
    driver.get(optionurl)
    wait = WebDriverWait(driver, 30)
    wait.until(
        EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, "ul.SearchList_SearchList__PL2mv")
        )
    )

    page_num = 1
    detail_url_list = []

    while True:
        try:
            if page_num == 4:
                break
            pageurl = f"{optionurl}&pageIndex={page_num}"
            driver.get(pageurl)
            wait.until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, "ul.SearchList_SearchList__PL2mv")
                )
            )
            detail_url = driver.find_elements(
                By.CSS_SELECTOR, "a.SearchList_anchor__zbpU4"
            )
            for url in detail_url:
                detail_url_list.append(url.get_attribute("href"))
            page_num += 1
        except Exception as e:
            print("페이지 오류 발생", e)
            break

    return detail_url_list
