import selenium
from selenium import webdriver as wb
webD = wb.Chrome()
webD.get("https://www.pinterest.com/Marcellthekid/men-fashion-catalog/")

from time import sleep
print("Please scroll down as far as possible for 20 seconds")
sleep(20)

productInfoList = webD.find_elements_by_class_name("GrowthUnauthPinImage")

img_links = []

for el in productInfoList:
    pp1 = el.find_element_by_tag_name("a")
    pp2 = pp1.find_element_by_tag_name("img")
    img_links.append(pp2.get_attribute("src"))

import pandas as pd
df_pintrest_men = pd.DataFrame(columns=["img_links"])
df_pintrest_men["img_links"] = img_links

df_pintrest_men.to_csv("df_pintrest_men.csv")
