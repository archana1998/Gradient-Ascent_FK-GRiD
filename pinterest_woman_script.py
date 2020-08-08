import selenium
from selenium import webdriver as wb
webD = wb.Chrome()
webD.get("https://www.pinterest.com/Kuricho/womens-t-shirts/")

from time import sleep
print("Scroll down as far as possible for 20 seconds")
sleep(20)

productInfoList = webD.find_elements_by_class_name("GrowthUnauthPinImage")
img_links = []

for el in productInfoList:
    pp1 = el.find_element_by_tag_name("a")
    pp2 = pp1.find_element_by_tag_name("img")
    img_links.append(pp2.get_attribute("src"))
    print("added")

import pandas as pd
df_pinterest_women = pd.DataFrame(columns=["img_links"])
df_pinterest_women["img_links"] = img_links
df_pinterest_women

df_pinterest_women.to_csv("df_pinterest_women.csv")