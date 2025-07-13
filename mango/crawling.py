from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

def fetch_full_html(url, output_path="full_page.html"):
    # 브라우저 옵션 설정 (필요하면 headless로도 가능)
    options = Options()
    # options.add_argument("--headless")  # 필요 시 주석 해제
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    # 드라이버 실행
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(5)  # JS 로딩 대기 (필요에 따라 늘릴 수 있음)

        html = driver.page_source
        return html

    finally:
        driver.quit()


product_url = "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000170266&dispCatNo=90000010001&trackingCd=Home_Curation1_1&curation=like&egcode=a016_a016&rccode=pc_main_01_c&egrankcode=10&t_page=%ED%99%88&t_click=%ED%81%90%EB%A0%88%EC%9D%B4%EC%85%981_%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=1"
soup = fetch_full_html(product_url)

for dt in soup.find_all("dt"):
    if "화장품법에 따라 기재해야 하는 모든 성분" in dt.get_text():
        dd = dt.find_next_sibling("dd")
        if dd:
            ingredients = dd.get_text(strip=True)
            print("✅ 전성분:", ingredients)
        else:
            print("❌ dd 태그를 찾을 수 없습니다.")
        break