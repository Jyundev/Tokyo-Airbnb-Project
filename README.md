# 도쿄 에어비엔비 숙소 추천 프로젝트

## 🔥 구성원

| 구성원 | 깃허브 주소 | 역할 |  
| --- | --- | --- | 
| 이지은 | https://github.com/zinnie1025 | Project Leader |
| 장윤영 | https://github.com/Jyundev | Project Manager |

</br></br>

## 🖥️  Environment 
**비고** | **이지은(local)** | **이지은(local)** | **장윤영(local)** | **장윤영(local)**
-----|-------|-------|-------|-------|
**CPU** | Intel Core i9 | AMD Ryzen7-4 5800x | Intel Core i9 | i9-13900KF |
**RAM** | 16GB | 64GB | 16GB | 32GB |  
**Storage** | 1TB | 1TB | 1TB | 1TB |
**OS** | macOS | Windows 10 | macOS | Windows 11 |
**모바일** | iPhone 14 Pro | - | iPhone 13 Mini | - |

</br>

| Stack | Tools | Collaboration |
|-------|-------|---------------|
| <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSHLN0RrPTmNUSMhl6MTeX0p_uIIj6Qzoxok9gjmzjELFRCeJaN34K8nOSaG56rrrw-evQ&usqp=CAU" alt="Python" width="40px"> Python | <img src="https://git-scm.com/images/logos/downloads/Git-Icon-1788C.png" alt="Git" width="40px"> Git<br><br><img src="https://logowik.com/content/uploads/images/google-colaboratory6512.jpg" alt="Colab" width="40px"> Colab | <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub" width="40px"> GitHub<br><img src="https://cdn.icon-icons.com/icons2/2389/PNG/512/notion_logo_icon_145025.png" alt="Notion" width="40px"> Notion<br><img src="https://cdn-icons-png.flaticon.com/512/2111/2111615.png" alt="Slack" width="40px"> Slack |


</br></br>


## Contents Table

- [프로젝트 개요](#📑-프로젝트-개요)
- [기대 효과](#🛎️-기대-효과)
- [프로젝트 설명](#✒️-프로젝트-설명)
- [모델 설명](#✒️-모델-설명)
- [Dataset](#📁-dataset)
- [Reference](#📌-reference)

</br></br>


## 📑 프로젝트 개요 

<div align="center" style="display: flex; justify-content: center; text-align: center;">
  <img src="img/news.png" alt="Alt text" style="width: 90%; margin: 5px;">
</div>

<br>

 에어비앤비를 통해 일본 여행을 계획 중에, "[일본 여행 갔을 때 수상하게 많이 싼 에어비앤비를 조심해야 하는 이유](https://kohwok.tistory.com/2747)"라는 게시글을 발견했습니다. 

해당 게시글은 주로 일본의 치안 상황을 잘 모르는 여행객들을 상대로, 호스트들이 치안이 좋지 않은 지역의 숙소를 극히 저렴한 가격에 제공하고 있다는 내용을 다루고 있었습니다.  후기에는 대부분의 한국인들이 좋은 별점과 함께 우호적인 평가를 작성하고 있어, 치안 위험 지역에도 한국인 여행객들이 많이 숙소를 예약하는 경향이 있었습니다.

실제로 에어비앤비를 확인한 결과, 가부키쵸와 산야지구 같은 위험 지역에서 저렴한 가격으로 숙소를 제공하는 사례가 있었습니다.

이에 따라, 여행객들에게 치안 정보를 추가하여 에어비앤비 숙소를 제공한다면, 더욱 안전하고 신뢰성 있는 선택을 할 수 있을 것으로 판단하여 해당 프로젝트를 기획하게 되었습니다

</br></br>

## 📆 프로젝트 목표 

| 기간 | 목표 |
| --- | --- |
| 1차 (2024.02.11 - 2024.02.28)| 데이터 수집 및 아키텍처 설계, 전체 플로우 설계, 수집 데이터 전처리 |
|2차 (2024.03.01 - 2024.03.23) | 도쿄 여행 최단 경로 알고리즘(필수), 공항 포함 경로(옵션) |
| 3차 (2024.03.24 - 2024.04.30) | 도쿄 안전 숙소 정보 제공(필수), 도쿄 여행 명소 실시간 티켓가(옵션)|

</br></br>

## 🛎️ 기대 효과
- 각 지역에 대한 치안 등급을 부여
    > 치안 데이터를 활용하여 각 지역의 상대적인 안전 수준을 판단합니다
- 안전 숙소 제안 
    > 치안 등급을 기반으로하여 여행객들에게 안전한 숙소를 추천합니다. 
- 숙소까지 최단 거리 경로 제공 
    >선택된 숙소까지 안전하고 효율적으로 이동할 수 있는 최단 거리 경로를 제공합니다. 

</br></br>

## ✒️  프로젝트 설명

<div align="center" style="display: flex; justify-content: center; text-align: center;">
  <img src="img/flow.png" alt="Alt text" style="width: 90%; margin: 5px;">
</div>

</br></br>

## 📁 Dataset

| Title | link |
| --- | --- |
| Airbnb| <a href = http://insideairbnb.com/get-the-data>에어비앤비 도쿄 데이터</a> |
| 도쿄 부동산 사건 데이터  | <a href = http://www.oshimaland.co.jp>오시마랜드</a>|
| 도쿄 공공 데이터 |<a href = http://www.oshimaland.co.jp>절도 데이터 </a> |
