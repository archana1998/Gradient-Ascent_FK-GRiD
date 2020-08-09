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

### Requirements 
 - Python 3.6
 - Selenium
 - Keras
 - TensorFlow
 - Matplotlib
 - Sklearn
 - Numpy
 - Pandas

### 1. Web Scraping
 - This was done using Selenium with Python3
 - We chose 6 locations to scrape images from, covering a range of multipurpose e-Commerce sites, fashion magazines, catalogues and fashion shopping sites
	 - Vogue India
	 - Flipkart
	 - Myntra 
	   (above 3 can be accessed by running the ```data_collection_fkmyvog.py```)
	 - Amazon (run ```amazon_data_script.py```)
	 - Pinterest Womens Fashion catalogue (run ```pinterest_woman_script.py```)
	 - Pinterest Mens Fashion catalogue (run ```pinterest_man_script.py```)
	 
 - From sites like Flipkart and Amazon, we extracted the product name, rating, number of reviews and the image
 - From the other sites, we extracted the fashion images
 - The scripts can be easily modified to work on other websites by just changing a few variables according to the architecture of the website, hence this step can be easily scaled up
 - All of the data scraped is converted to Pandas dataframe and then stored as a CSV
 
 ### 2. Downloading the images and Object Detection
 - The images can be downloaded from the image links stored in the CSV by running the ``` image_download_script.py ```
 - Object Detection was done using a pretrained YOLOv3 architecture that was trained with the DeepFashion2 dataset
 - Code is available at this repository (https://github.com/archana1998/Clothing-Detection), and can be cloned and used by just running the ```new_image_demo.py``` script
 - This model identifies "long and short top" object categories and crops out just the bounding box of the image, that contains only the t-shirt.
 - The t-shirt image is then saved and used for feature extraction

### 3. Learning Feature Encodings
 - In order to represent our images for later processing, we needed a way to extract the features from each clothing item
 - We trained a model using the keras library and tensorflow backend
 - Our model was based on the CNN architecture which is known in the Computer Vision world for being able to learn features from images
 - We recreated some of the images using the encodings we got and the results were very promising, indicating that out feature encodings/representations are accurate
 - To create the model, run the script `encoder_training_script.py`
 - Alternatively, download the trained model from - https://drive.google.com/file/d/1_ZRFLLusck_1waFl703PK0oDas7NWo0n/view?usp=sharing

### 4. Computing the Popularity Metric (PM)
 - We wanted consider both ratings and the number of ratings in our attempt to rank all the products effectively
 - We came up with a popularity measure which combines the two properly
 -  A Bayesian view of the beta distribution was adopted to come up with a formula to give us a PM given the rating and number of ratings
**![](https://lh4.googleusercontent.com/YHqDVGGew38M4WKuhsW26LaNQocchnEG5CwgMOthi_hWGc2UE4fpkMsuMd1afKd74_c5Qeiss5ZOL6wVp0TvMMUK77mYnj7VLtIwfJ05ncfCf5MuMGC0PyrdJSCdsgqrekdNtoTamfE)**
 - We loaded in all our e-Commerce data, calculated the feature encodings using the model mentioned earlier
 - Then computed the PM for each product
 - Then trained a model to predict the PM given a set of encodings - we can now compare the predicted performance of different products on e-Commerce sites, this is especially useful for designers that want to know how the public would react to their clothes
 - To create and train the model, run `pm_model_train_script.py`
 - Alternatively, you can download the trained model from here - https://drive.google.com/file/d/1QiyeRfWD18GAdJl-lUMxjvp6LF_amTl1/view?usp=sharing
 - Once the model is created, you can run `pm_predictor_script.py` to predict the PM for any input image
 
 ### 5. Clustering
 - Using the encodings previously calculated, we performed clustering on a selection of images determined by the user to visualise the trending and lagging products in the set of images being considered
 - 5 clustering algorithms were tested and evaluated using the Silhouette coefficient and K means clustering gave us the best results
 - We took the largest cluster to be a representation of the most popular/trending styles of clothes and the smallest clusters to be a representation of what isn't popular
 - This can be tested by running `clustering_script.py`


### Running instructions
1) Create an environment with all the packages and libraries specified in the "requirements" section
2) Download the "Zipped_final.zip" folder from here - https://drive.google.com/file/d/1WI95J600swejVn2-6vzhFRuxKfZa_gQh/view?usp=sharing
3) Download the encoder model from here - https://drive.google.com/file/d/1_ZRFLLusck_1waFl703PK0oDas7NWo0n/view?usp=sharing
4) Download the PM predictor model from here - https://drive.google.com/file/d/1QiyeRfWD18GAdJl-lUMxjvp6LF_amTl1/view?usp=sharing
5) Run `clustering_script.py` to replicate the clustering step and to visualise trends and lags in selected images from different sites
6) Run `pm_predictor_script.py` to calculate the expected PM of any input image given to the model

Note: These instructions are intended to get someone up and running with the application quickly and easily, alternatively you can choose to scrape data and train models from scratch using the respective scripts available in the repo
