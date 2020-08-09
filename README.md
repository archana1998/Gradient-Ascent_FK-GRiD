## Gradient Ascent - Flipkart GRiD 2020
Submission by -
Rushabh Musthyala,
Archana Swaminathan,
Shanmukh Kali Prasad 

### Problem Definition
A fashion retailer wants to source ongoing and upcoming fashion trends from major online fashion portals and online magazines in a consumable and actionable format, so that they are able to effectively and efficiently design an upcoming fashion product portfolio.

Deliverables -
1) A mechanism for effectively ranking products on e-Commerce sites
2) A way to analyse trending and lagging products on fashion portals and magazines
3) For the solution to be scalable   

### Subproblems 
1) Scraping data from e-Commerce websites and fashion portals
2) Cleaning image data to remove unwanted artifacts (extracting only images of shirts)
3) Learning feature encodings for all of the images
4) Computing a popularity metric (PM) to effectively combine the rating and number of reviews
5) Clustering the images based on their encodings to gain insight on what is trending and what is lagging

### 1. Web Scraping
 - This was done using Selenium with Python3
 - We chose 6 locations to scrape images from, covering a range of multipurpose e-Commerce sites, fashion magazines, catalogues and fashion shopping sites
	 - Vogue India
	 - Flipkart
	 - Amazon
	 - Pinterest Womens Fashion catalogue
	 - Pinterest Mens Fashion catalogue
	 - Myntra
 - From sites like Flipkart and Amazon, we extracted the product name, rating, number of reviews and the image
 - From the other sites, we extracted the fashion images
 - The scripts can be easily modified to work on other websites by just changing a few variables according to the architecture of the website, hence this step can be easily scaled up
 - All of the data scraped is converted to Pandas dataframe and then stored as a CSV
 
 ### 3. Downloading the images and Object Detection
 - The images can be downloaded from the image links stored in the CSV by running the ''' image_download_script.py '''
 - Object Detection was done using a pretrained YOLOv3 architecture that was trained with the DeepFashion2 dataset
 - Code is available at this repository (https://github.com/archana1998/Clothing-Detection), and can be cloned and used by following instructions in the README of the file.
 - This model identifies "long and short top" object categories and crops out just the bounding box of the image, that contains only the t-shirt.
 - The t-shirt image is then saved and used for feature extraction
