import numpy as np
import matplotlib.pyplot as plt
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D, Flatten
from keras.models import Model
from keras import backend as K
import tensorflow.keras.layers
import keras
import os
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

encoder = tf.keras.models.load_model('encoder', compile=False)

import zipfile

zip_ref = zipfile.ZipFile("Zipped_final.zip", 'r')
zip_ref.extractall("/tmp")
zip_ref.close()

from skimage.transform import resize
from skimage.io import imread_collection

def get_amazon():
  col_dir = '/tmp/Zipped/Amazon Images/*.jpg'
  col_amazon = imread_collection(col_dir)
  col_amazon = list(col_amazon)

  for i in range(len(col_amazon)):
    col_amazon[i] = resize(col_amazon[i], (320, 192, 3))
  return col_amazon

def get_flipkart():
  col_dir = '/tmp/Zipped/Flipkart Images/*.jpg'
  col_fk = imread_collection(col_dir)
  col_fk = list(col_fk)

  for i in range(len(col_fk)):
    col_fk[i] = resize(col_fk[i], (320, 192, 3))
  return col_fk

def get_myntra():
  col_dir = '/tmp/Zipped/Myntra Images/*.jpg'
  col_myntra = imread_collection(col_dir)
  col_myntra = list(col_myntra)

  for i in range(len(col_myntra)):
      col_myntra[i] = resize(col_myntra[i], (320, 192, 3))
  return col_myntra

def get_pinmen():
  col_dir = '/tmp/Zipped/Pinterest Men Images/*.jpg'
  col_pinmen = imread_collection(col_dir)
  col_pinmen = list(col_pinmen)

  for i in range(len(col_pinmen)):
      col_pinmen[i] = resize(col_pinmen[i], (320, 192, 3))
  return col_pinmen

def get_pinwomen():
  col_dir = '/tmp/Zipped/Pinterest Women Images/*.jpg'
  col_pinwom = imread_collection(col_dir)
  col_pinwom = list(col_pinwom)

  for i in range(len(col_pinwom)):
      col_pinwom[i] = resize(col_pinwom[i], (320, 192, 3))
  return col_pinwom

def get_vogue():
  col_dir = '/tmp/Zipped/Vogue Images/*.jpg'
  col_vog = imread_collection(col_dir)
  col_vog = list(col_vog)

  for i in range(len(col_vog)):
      col_vog[i] = resize(col_vog[i], (320, 192, 3))
  return col_vog

print("You can choose out of - ")
print("1. amazon (Amamzon)")
print("2. flipkart (Flipkart)")
print("3. myntra (Myntra)")
print("4. pinmen (Pinterest Men)")
print("5. pinwom (Pinterest Women)")
print("6. vogue (Vogue)")

user_input = input("Please enter your choices(separated by a comma): ")
user_input = user_input.split(",")

col_cluster = []
for cat in user_input:
  if "pinmen" == cat:
    col_cluster += get_pinmen()
  elif "pinwom" == cat:
    col_cluster += get_pinwomen()
  elif "vogue" == cat:
    col_cluster += get_vogue()
  elif "myntra" == cat:
    col_cluster += get_myntra()
  elif "amazon" == cat:
    col_cluster += get_amazon()
  elif "flipkart" == cat:
    col_cluster += get_flipkart()

print("Data collected successfully")

col_cluster = np.array(col_cluster)

encodings = encoder.predict(col_cluster)
flattened_encodings = []

for en in encodings:
  en = en.flatten()
  flattened_encodings.append(en)

print("Encodings calculated")

from sklearn.cluster import KMeans

clusters = int(len(flattened_encodings)/10)
kmeans = KMeans(n_clusters=clusters, init='k-means++', max_iter=500, n_init=10, random_state=0)

pred_y = kmeans.fit_predict(flattened_encodings)

print("Clustering complete")

from collections import Counter

list_freq= (Counter(pred_y))
list_freq = sorted(list_freq.items(), key=lambda x: x[1], reverse=True)
trend = list_freq[0][0]

lagging = []
for i in range(clusters-clusters//10, clusters):
    lagging.append(list_freq[i][0])

frequent_imgs = []
lagging_imgs = []
for i in range(len(pred_y)):
    if pred_y[i] == trend:
        frequent_imgs.append(i)
    if pred_y[i] in lagging:
        lagging_imgs.append(i)

import os

directory = "cluster_trends"
img_path = os.path.join(directory) 
if(os.path.isdir(img_path)==False):
    os.mkdir(img_path)
    print("Directory '% s' created" % directory) 

directory = "cluster_lags"
img_path = os.path.join(directory) 
if(os.path.isdir(img_path)==False):
    os.mkdir(img_path)
    print("Directory '% s' created" % directory) 

from skimage.io import imsave

for j in range(len(frequent_imgs)):
    img = (col_cluster[frequent_imgs[j]]*255).astype(np.uint8)
    path = 'cluster_trends/'+str(j)+'.jpg'
    imsave(path, img)

for j in range(len(lagging_imgs)):
    img = (col_cluster[lagging_imgs[j]]*255).astype(np.uint8)
    path = 'cluster_lags/'+str(j)+'.jpg'
    imsave(path, img)

print("Done! Most popular images are saved on your device!")


