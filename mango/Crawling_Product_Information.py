from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import pyautogui
import csv

#html parsing
def fetch_full_html(url, output_path="full_page.html"):
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        
        pyautogui.moveTo(1168, 1298, duration=1)  #Physical coordinates
        time.sleep(3)  #Time to go beyond security
        pyautogui.scroll(-620)
        time.sleep(4)  #Page loading time
        pyautogui.leftClick()
        time.sleep(0.5)  #Click time
        html = driver.page_source

        return html

    finally:
        driver.quit()

wanted_keys = [
    "사용기한(또는 개봉 후 사용기간)",
    "사용방법",
    "화장품법에 따라 기재해야 하는 모든 성분"
]

key_name_map = {
    "사용기한(또는 개봉 후 사용기간)": "사용기한",
    "사용방법": "사용방법",
    "화장품법에 따라 기재해야 하는 모든 성분": "성분"
}

#Find product details
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
    
    #Change to desired format
    filtered_info = {k: product_info[k] for k in wanted_keys if k in product_info}
    final_info = {key_name_map[k]: v for k, v in filtered_info.items()}
    asd = final_info['성분']
    ingredients = asd.split(",")
    final_info['성분'] = ingredients 
    
    #Save only the parts you want
    with open("filtered_product_info.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["항목", "내용"])
        for key, value in final_info.items():
            writer.writerow([key, value])
    return product_info

product_url = "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000170266&dispCatNo=90000010001"
html = fetch_full_html(product_url)
info = parse_product_info(html)

print(" 상품 상세 정보:")
for key, value in info.items():
    print(f"{key} : {value}")
