from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import pyautogui
import csv
import pandas as pd
import Crawling_Product_Information as CPI
import os

files = os.listdir('url')

prd_dict = {}
os.chdir(r'C:\Users\leeks\my_git\url')
for i in files:
    Temporary_list = []
    read_csv = pd.read_csv(i)
    for i in range(len(read_csv)):
        Temporary_list.append(read_csv.iloc[i,1])
        prd = read_csv.iloc[i,0]
    prd_dict[prd] =Temporary_list
print(prd_dict.keys())
a = input('원하는 항목 선택')

Category_List = a.split(' ')
Category_dict = {a:prd_dict[a] for a in Category_List}

b = []
df = pd.DataFrame(columns=['제품명', '가격', '사용기한', '사용방법', '카테고리'])
a = 0
for k,v in Category_dict: 
    for url in v:
        html = CPI.fetch_full_html(url)
        info, ingredient = CPI.parse_product_info(html, k)
        b.append(ingredient)
        df.loc[len(df)] = info
        a += 1
        if a == 5:
            break
    break

df2 = pd.DataFrame(b)
print(df2)
print(df)
df.to_csv('C:/Users/leeks/OneDrive/바탕 화면/csv/output.csv', index=False)
df2.to_csv('C:/Users/leeks/OneDrive/바탕 화면/csv/output1.csv', index=False)