import selenium
from selenium import webdriver as wb
import pandas as pd

def get_flipkart():
	webD = wb.Chrome()
	webD.get("https://www.flipkart.com/clothing-and-accessories/topwear/tshirt/men-tshirt/pr?sid=clo,ash,ank,edy&otracker=categorytree&otracker=nmenu_sub_Men_0_T-Shirts")

	links = []
	names = []
	ratings = []
	no_revs_list = []
	img_links = []
	count = 1
	while(count < 25):
		productInfoList = webD.find_elements_by_class_name("_2mylT6")
		for el in productInfoList:
		    link = el.get_attribute("href")
		    links.append(link)
		    
		next_page = webD.find_elements_by_class_name("_3fVaIS")[-1]
		webD.get(next_page.get_attribute("href"))
		count += 1

	for link in links:
		webD.get(link)
		try:
		    name = webD.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span[2]").text
		    rating = webD.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[3]/div/div/span[1]/div").text
		    no_revs = webD.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[3]/div/div/span[2]").text
		    no_revs = no_revs.split()[0]
		    img_link = webD.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[2]/div/img").get_attribute("src")
		    names.append(name)
		    ratings.append(rating)
		    no_revs_list.append(no_revs)
		    img_links.append(img_link)
		except:
		    pass
		try:
		    name = webD.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span[2]").text
		    rating = webD.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[4]/div/div/span[1]/div").text
		    no_revs = webD.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[4]/div/div/span[2]").text
		    no_revs = no_revs.split()[0]
		    img_link = webD.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[2]/div/img").get_attribute("src")
		    names.append(name)
		    ratings.append(rating)
		    no_revs_list.append(no_revs)
		    img_links.append(img_link)
		except:
		    pass

	df_flipkart = pd.DataFrame(columns=["name", "rating", "no_of_reviews", "img_links"])
	df_flipkart["name"] = names
	df_flipkart["rating"] = ratings
	df_flipkart["no_of_reviews"] = no_revs_list
	df_flipkart["img_links"] = img_links

	df_flipkart.to_csv("df_flipkart.csv")
	

def get_vogue():
	webD = wb.Chrome()
	webD.get("https://www.vogue.in/vogue-closet/?closet=vogue_closet&filter_type=product_collection&order_by=recent&q=t+shirt&celebrity=&occasion=&price=&product-type=clothing")

	img_links = []
	i = 0
	while(i < 75):
		try:
		    productInfoList = webD.find_elements_by_class_name("product-wrapper")
		    for el in productInfoList:
		        pp1 = el.find_element_by_tag_name("a")
		        pp2 = pp1.find_element_by_tag_name("img")
		        img_links.append(pp2.get_property("src"))
		    page_nav = webD.find_element_by_class_name("pagination")
		    butts = page_nav.find_elements_by_tag_name("a")[-1]
		    butts.click()
		except:
		    pass
		i += 1


	df_vogue = pd.DataFrame(columns=["img_links"])
	df_vogue["img_links"] = img_links

	df_vogue.to_csv("df_vogue.csv")


	

def get_myntra():
	webD = wb.Chrome()
	webD.get("https://www.myntra.com/tshirts")

	links = []
	i = 0
	while(i < 40):
		try:
		    productInfoList = webD.find_elements_by_class_name("product-base")
		    for el in productInfoList:
		        pp1 = el.find_element_by_tag_name("a")
		        links.append(pp1.get_attribute("href"))
		    nav = webD.find_element_by_xpath("/html/body/div[2]/div/div[1]/main/div[3]/div[2]/div/div[2]/section/div[2]/ul")
		    butt = nav.find_elements_by_tag_name("li")[-1]
		    butt_anc = butt.find_element_by_tag_name("a")
		    butt_anc.click()
		except:
		    pass
		i += 1

	img_links = []
	for link in links:
		webD.get(link)
		try:
		    img_l = webD.find_element_by_xpath("/html/body/div[2]/div/div/div/main/div[2]/div[1]/div[1]/div/div[1]").get_attribute("style")[23:-3]
		    img_links.append(img_l)
		except:
		    pass

	df_myntra = pd.DataFrame(columns=["img_links"])
	df_myntra["img_links"] = img_links

	df_myntra.to_csv("df_myntra.csv")


#get_flipkart()
#get_myntra()
get_vogue()
