from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import pandas as pd

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import random
from datetime import date, timedelta

engine = create_engine("postgresql://genie:지은비번5@지은IP주소:5432/airbnb")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class NaverTrip(Base):
    __tablename__ = "navertokyotrip"

    id = Column(Integer, primary_key=True)
    checkin_date = Column(Date)
    checkout_date = Column(Date)
    adultnum = Column(Integer)
    childnum = Column(Integer)
    korean_name = Column(String)
    english_name = Column(String)
    address = Column(String)
    price = Column(Integer)


Base.metadata.create_all(engine)


def generate_random_dates():
    """
    사용자 입력을 랜덤으로 받아 자동으로 수집하기 위한 함수

    author : 이지은
    updated date : 240229
    """
    start_date = date(2024, 3, 1)
    end_date = date(2024, 4, 30)
    delta = end_date - start_date
    random_days_to_add = random.randint(0, delta.days)
    checkin_date = start_date + timedelta(days=random_days_to_add)
    checkout_date = checkin_date + timedelta(days=random.randint(1, 4)) 
    return checkin_date, checkout_date


def get_optionurl(checkin_date, checkout_date, adultnum, childnum):
    """
    체크인, 체크아웃, 성인(만 18세 이상), 어린이(만 18세 미만) 인원 수에 따른 숙소 정보 수집

    input : 체크인 날짜, 체크아웃 날짜, 성인 수, 어린이 수
    output : 숙소 정보(숙소 한국어명, 숙소 영어명, 숙소 주소, 숙소 가격)
    author : 이지은
    updated date : 240225
    last updated : 240228

    """
    baseurl = "https://hotels.naver.com/"

    if int(childnum) > 0:
        child_age_list = []
        for _ in range(int(childnum)):
            child_age_list.append(
                str(random.randint(0, 17))  
            )
        optionurl = (
            f"{baseurl}list?placeFileName=place%3ATokyo&&adultCnt={(adultnum)}"
            + "&childAges="
            + "%2C".join(child_age_list)
            + f"&checkIn={(checkin_date)}&checkOut={(checkout_date)}&includeTax=false&sortField=popularityKR&sortDirection=descending"
        )
    else:
        optionurl = f"{baseurl}list?placeFileName=place%3ATokyo&&adultCnt={adultnum}&checkIn={(checkin_date)}&checkOut={(checkout_date)}&includeTax=false&sortField=popularityKR&sortDirection=descending"
    print(f"Go to option Link : {optionurl}")
    return optionurl


def get_detailurl(optionurl):
    """
    숙소 상세 정보 url
    """
    driver = webdriver.Chrome()
    driver.get(optionurl)
    wait = WebDriverWait(driver, 20)

    wait.until(
        EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, "ul.SearchList_SearchList__PL2mv")
        )
    )

    page_num = 1
    detail_url_list = []

    while True:
        try:
            if page_num == 3:
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

    driver.quit()
    return detail_url_list


def get_accommodation_info(driver, url):
    """
    숙소 이름, 주소, 가격 수집
    """
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    korea_name_element = driver.find_element(
        By.CSS_SELECTOR, "strong.common_name__R4vrb"
    )
    korean_name = (
        korea_name_element.text.strip() if korea_name_element else "Name Not Found"
    )

    english_name_element = driver.find_element(By.CSS_SELECTOR, "i.common_eng__t2GFX")
    english_name = (
        english_name_element.text.strip() if english_name_element else "Name Not Found"
    )

    address_element = driver.find_element(
        By.CSS_SELECTOR, "ul.common_infoList__mJYps > li:nth-child(1) span"
    )
    address = (
        address_element.text.strip().replace(", 일본  위치", "")
        if address_element
        else "Address Not Found"
    )

    price_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "em.common_price__l_LpX"))
    )
    price = (
        int(price_element.text.strip().replace(",", "").replace("원", "").rstrip())
        if price_element
        else -1
    )

    return korean_name, english_name, address, price


if __name__ == "__main__":
    print("Welcome to Tokyo Accommodation Information System")
    print("===============================================")

    """사용자 입력을 직접 할 때
    # checkin_date = input("Enter the check-in date (YYYY-MM-DD format): ")
    # checkout_date = input("Enter the check-out date (YYYY-MM-DD format): ")
    # adultnum = input("Enter the number of adults: ")
    # childnum = input("Enter the number of children: ")
    """
    driver = webdriver.Chrome()
    for _ in tqdm(range(10)):
        checkin_date, checkout_date = generate_random_dates()
        adultnum = random.randint(1, 2)
        childnum = random.randint(0, 2)
        optionurl = get_optionurl(checkin_date, checkout_date, adultnum, childnum)
        detail_urls = get_detailurl(optionurl)

        with Session() as session:
            for url in tqdm(detail_urls):
                try:
                    accommodation_info = get_accommodation_info(driver, url)
                    session.add(
                        NaverTrip(
                            checkin_date=checkin_date,
                            checkout_date=checkout_date,
                            adultnum=adultnum,
                            childnum=childnum,
                            korean_name=accommodation_info[0],
                            english_name=accommodation_info[1],
                            address=accommodation_info[2],
                            price=accommodation_info[3],
                        )
                    )
                except Exception as e:
                    print(f"Error fetching accommodation info for URL {url}: {e}")
            session.commit()

    print("\nData collection completed.")
