import pandas as pd
import numpy as np
import tensorflow as tf

encoder = tf.keras.models.load_model('encoder', compile=False)

import zipfile

zip_ref = zipfile.ZipFile("Zipped_final.zip", 'r')
zip_ref.extractall("/tmp")
zip_ref.close()

df_amazon = pd.read_csv("/tmp/Zipped/df_amazon.csv", thousands=',')
df_flipkart = pd.read_csv("/tmp/Zipped/df_flipkart.csv", thousands=',')

df_amazon = df_amazon.drop(columns=["Unnamed: 0"])
df_flipkart = df_flipkart.drop(columns=["Unnamed: 0"])

for i in range(len(df_amazon)):
  try:
    df_amazon.iloc[i][1] = df_amazon.iloc[i][1].split(" ")[0]
  except:
    pass
  try:
    df_amazon.iloc[i][2] = df_amazon.iloc[i][2].split(" ")[0].replace(",", "")
  except:
    pass
df_amazon.head()

df_amazon["rating"] = df_amazon["rating"].astype('float32')
df_amazon["no_of_reviews"] = df_amazon["no_of_reviews"].astype('int32')

import matplotlib.image as mpimg

fk_imgs = []
deletes = []

for i in range(len(df_flipkart)):
  name = "/tmp/Zipped/Flipkart Images/crop_"+str(i)+'.jpg'
  try:
    img = mpimg.imread(name)
    fk_imgs.append(img)
  except:
    deletes.append(i)

df_flipkart = df_flipkart.drop(deletes)
from skimage.transform import resize
for i in range(len(fk_imgs)):
  fk_imgs[i] = resize(fk_imgs[i], (320, 192, 3))

fk_encodings = encoder.predict(np.array(fk_imgs))

flattened_fk = []

for en in fk_encodings:
  en = en.flatten()
  flattened_fk.append(en)

df_flipkart["encodings"] = flattened_fk

ama_imgs = []
deletes = []

for i in range(len(df_amazon)):
  name = "/tmp/Zipped/Amazon Images/crop_"+str(i)+'.jpg'
  try:
    img = mpimg.imread(name)
    ama_imgs.append(img)
  except:
    deletes.append(i)

df_amazon = df_amazon.drop(deletes)

for i in range(len(ama_imgs)):
  ama_imgs[i] = resize(ama_imgs[i], (320, 192, 3))

ama_encodings = encoder.predict(np.array(ama_imgs))

flattened_ama = []

for en in ama_encodings:
  en = en.flatten()
  flattened_ama.append(en)

df_amazon["encodings"] = flattened_ama

df_combined = pd.concat([df_amazon, df_flipkart])

df_combined = df_combined.dropna()
df_combined = df_combined.reset_index().drop(columns=["index"])

def pop_met(n, s):
    top = s*(15+n)*1.0
    bott = n+5*s*1.0
    pm = top/bott
    return pm

df_combined["popularity"] = pop_met(df_combined["no_of_reviews"], df_combined["rating"])

X = list(df_combined["encodings"])
y = list(df_combined["popularity"])

X = np.array(X)
y = np.array(y)
y = y.reshape(1992, 1)

from keras.models import Sequential
from keras.layers import Dense

model = Sequential()

model.add(Dense(1920, input_dim=1920, activation='relu'))
model.add(Dense(1024, activation='relu'))
model.add(Dense(512, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(1))

model.compile(loss='mse', optimizer='adam', metrics=['mae', 'mse'])

model.fit(np.asarray(X), np.asarray(y), batch_size=32, epochs=50, validation_split=0.2)

model.save("pm_model")

df_sorted = df_combined.sort_values(by=['popularity'], ascending=False)
df_sorted.to_csv("df_sorted.csv")
