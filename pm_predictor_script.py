import matplotlib.image as mpimg
import pandas as pd
import numpy as np
import tensorflow as tf
from skimage.transform import resize
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#Loading the encoder and predictor models
encoder = tf.keras.models.load_model('encoder', compile=False)
pm_model = tf.keras.models.load_model('pm_model', compile=False)

while(True):
	#Take the input image
	path = input("Please enter the path of the image you want to check (type exit to end): ")
	if(path == "exit"):
		break
	img = mpimg.imread(path)
	img = resize(img, (320, 192, 3))

	#Find the encoding for it
	temp_arr = []
	temp_arr.append(img)
	img_enc = encoder.predict(np.array(temp_arr))
	flattened_enc = img_enc.flatten()

	#Predict its popularity
	pm_prob = pm_model.predict(np.array([flattened_enc]))
	pm_prob = pm_prob[0][0]
	print("The predicted popularity is", pm_prob)
