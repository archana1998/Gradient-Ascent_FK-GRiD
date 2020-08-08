import selenium
from selenium import webdriver as wb
webD = wb.Chrome()
webD.get("https://www.amazon.in/s?k=t-shirts&i=apparel&bbn=1968123031&rh=n%3A1968120031%2Cn%3A1968123031%2Cp_72%3A1318479031&dc&qid=1596720041&rnid=1318475031&ref=sr_nr_p_72_4")

count = 1
links = []
import time
while(count < 30):
    productInfoList = webD.find_elements_by_class_name("s-image-overlay-white-semitransparent")
    for el in productInfoList:
        pp1 = el.find_element_by_tag_name("span")
        pp2 = pp1.find_element_by_tag_name("a")
        links.append(pp2.get_property("href"))
    try:
        temp = webD.find_element_by_class_name("a-pagination")
        butt = temp.find_elements_by_tag_name("li")[-1]
        butt.find_element_by_tag_name("a").click()
    except:
        pass
    time.sleep(2)
    count += 1

names = []
ratings = []
no_revs_list = []
img_links = []

for link in links:
    webD.get(link)
    time.sleep(3)
    try:
        name = webD.find_element_by_xpath("/html/body/div[2]/div[2]/div[4]/div[1]/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/h1/span").text
        rating = webD.find_element_by_xpath("/html/body/div[2]/div[2]/div[4]/div[23]/div/div[1]/div[2]/div[1]/div/div[2]/div/span/span").text
        img_link = webD.find_element_by_xpath("/html/body/div[2]/div[2]/div[4]/div[1]/div[2]/div[1]/div/div[1]/div/div/div[2]/div[1]/div[1]/ul/li[1]/span/span/div/img").get_attribute("src")
        no_revs = webD.find_element_by_xpath("/html/body/div[2]/div[2]/div[4]/div[1]/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[4]/div/span[3]/a/span").text
        names.append(name)
        ratings.append(rating)
        no_revs_list.append(no_revs)
        img_links.append(img_link)
    except:
        try:
            name = webD.find_element_by_xpath("/html/body/div[2]/div[2]/div[4]/div[1]/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/h1/span").text
            rating = webD.find_element_by_xpath("/html/body/div[2]/div[2]/div[4]/div[1]/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[4]/div/span[1]/span/span[1]/a/i[1]/span").text
            img_link = webD.find_element_by_xpath("/html/body/div[2]/div[2]/div[4]/div[1]/div[2]/div[1]/div/div[1]/div/div/div[2]/div[1]/div[1]/ul/li[1]/span/span/div/img").get_attribute("src")
            no_revs = webD.find_element_by_xpath("/html/body/div[2]/div[2]/div[4]/div[1]/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[4]/div/span[3]/a/span").text
            names.append(name)
            ratings.append(rating)
            no_revs_list.append(no_revs)
            img_links.append(img_link)
        except:
            pass
                     

import pandas as pd
df_amazon = pd.DataFrame(columns=["name", "rating", "no_of_reviews", "img_links"])
df_amazon["name"] = names
df_amazon["rating"] = ratings
df_amazon["no_of_reviews"] = no_revs_list
df_amazon["img_links"] = img_links

df_amazon.to_csv("df_amazon.csv")           
