from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import time
import pandas as pd

# TODO : 도쿄 여행 숙소 정보 수집


def get_optionurl(checkin_date, checkout_date, adultnum, childnum):
    """
    체크인, 체크아웃, 성인(만 18세 이상), 어린이(만 18세 미만) 인원 수에 따른 숙소 정보 수집

    input : 체크인 날짜, 체크아웃 날짜, 성인 수, 어린이 수
    output : 숙소 정보(숙소 한국어명, 숙소 영어명, 숙소 주소, 숙소 가격)
    author : 이지은
    updated date : 240225
    """
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


def get_accommodation_name(driver, url):
    """
    숙소 이름, 주소, 가격 수집
    """
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    korea_name_element = driver.find_element(
        By.CSS_SELECTOR, "strong.common_name__R4vrb"
    )
    korea_name = (
        korea_name_element.text.strip() if korea_name_element else "Name Not Found"
    )

    english_name_element = driver.find_element(By.CSS_SELECTOR, "i.common_eng__t2GFX")
    english_name = (
        english_name_element.text.strip() if english_name_element else "Name Not Found"
    )

    address_element = driver.find_element(
        By.CSS_SELECTOR, "ul.common_infoList__mJYps > li:nth-child(1) span"
    )
    address = address_element.text.strip() if address_element else "Address Not Found"

    price_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "em.common_price__l_LpX"))
    )
    price = price_element.text.strip() if price_element else "Price Not Found"

    return korea_name, english_name, address, price


if __name__ == "__main__":
    print("Welcome to Tokyo Accommodation Information System")
    print("===============================================")

    checkin_date = input("Enter the check-in date (YYYY-MM-DD format): ")
    checkout_date = input("Enter the check-out date (YYYY-MM-DD format): ")
    adultnum = input("Enter the number of adults: ")
    childnum = input("Enter the number of children: ")

    print(f"\nTravel Details:")
    print(f"Check-in Date: {checkin_date}")
    print(f"Check-out Date: {checkout_date}")
    print(f"Number of Adults: {adultnum}")
    print(f"Number of Children: {childnum}")

    optionurl = get_optionurl(checkin_date, checkout_date, adultnum, childnum)
    detailurl = get_detailurl(optionurl)

    driver = webdriver.Chrome()
    accommodation_list = []

    for url in tqdm(detailurl):
        accommodation_info = get_accommodation_name(driver, url)
        accommodation_list.append(accommodation_info)

    driver.quit()

    print("\nAccommodation List:")
    for idx, info in enumerate(accommodation_list):
        print(f"{idx}. {info[0]} - {info[1]} - {info[2]} - {info[3]}")

    tokyo_accommodations = pd.DataFrame(
        accommodation_list, columns=["한국어 숙소명", "영어 숙소명", "주소", "가격"]
    )

    tokyo_accommodations.to_csv("tokyo_accomodations.csv", index=False)
