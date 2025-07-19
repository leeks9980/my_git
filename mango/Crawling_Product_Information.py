from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

def fetch_full_html(url, output_path="full_page.html"):
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(10) 

        html = driver.page_source

        return html

    finally:
        driver.quit()

def parse_product_info(html):
    soup = BeautifulSoup(html, "html.parser")

    product_info = {}
    for dl in soup.select("#artcInfo dl.detail_info_list"):
        dt = dl.find("dt")
        dd = dl.find("dd")
        if dt and dd:
            title = dt.get_text(strip=True)
            content = dd.get_text(" ", strip=True)
            product_info[title] = content

    return product_info

product_url = "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000191214&dispCatNo=100000100070017&t_page=%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC%EA%B4%80&t_click=%ED%94%84%EB%9E%98%EA%B7%B8%EB%9F%B0%EC%8A%A4_%EC%A0%84%EC%B2%B4__%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=6"
html = fetch_full_html(product_url)
info = parse_product_info(html)

print(" 상품 상세 정보:")
for key, value in info.items():
    print(f"{key} : {value}")
