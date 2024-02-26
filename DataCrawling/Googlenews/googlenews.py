import urllib.request as req
from bs4 import BeautifulSoup
import urllib.parse as par
from urllib.request import Request
import pickle
import re

# TODO 구글 도쿄 메트로 뉴스 결과 수집


def open_dict(file_name):
    """
    수집한 도쿄 메트로 지하철 pickle 파일 읽기
    """
    with open(file_name, "rb") as f:
        dictionary = pickle.load(f)
    return dictionary


def pattern_regex(text):
    """
    파파고 api로 번역한 지하철 명 중 한국어만 남기고 제거
    """
    result = re.sub(r"[^가-힣]", "", text)
    return result


def news_headline_crawl(station_list):
    """
    도쿄 지하철 역 별 최근 1주일 뉴스 헤드라인 수집
    author : 이지은
    updated date : 240226
    """

#   headlines = []
#     try:
#         for station in station_list:
#             encoded_station = par.quote(station)
#             url = f"https://news.google.com/search?q={encoded_station}&hl=ko&gl=KR&ceid=KR%3Ako"
#             request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
#             code = req.urlopen(request_site)
#             soup = BeautifulSoup(code, "html.parser")

#             news_href = soup.select("div.XlKvRb > a")
#             for href in news_href[:10]:
#                 tmp = href["href"]
#                 move_link = "https://news.google.com/" + tmp
#                 each_link = req.urlopen(move_link).geturl()
#                 headers = Request(each_link, headers={"User-Agent": "Mozilla/5.0"})
#                 code_each_link = req.urlopen(headers)
#                 soup_each_link = BeautifulSoup(code_each_link, "html.parser")
#                 news_title = soup_each_link.select_one("h1")
#                 print(news_title.text)
#                 headlines.append(news_title)
#     except Exception as e:
#         print("An error occurred:", str(e))
#     return headlines