import numpy as np
import matplotlib.pyplot as plt

from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D, Flatten
from keras.models import Model
from keras import backend as K
import tensorflow.keras.layers
import keras

#Defining the input image size - chosen so it can be recreated easily
input_img = Input(shape=(320, 192, 3))

#Model architecture definition
#Consists of convultional layers to help learn the features of the clothing item - sleeve type, striped, collar type, etc
x = Conv2D(64, (3, 3), activation='relu', padding='same')(input_img)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(16, (3, 3), activation='relu', padding='same')(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
encoded = MaxPooling2D((2, 2), padding='same')(x)

x = Conv2D(8, (3, 3), activation='relu', padding='same')(encoded)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
x = Conv2D(16, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
decoded = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

autoencoder = Model(input_img, decoded)

optimizer = keras.optimizers.Adam(lr=0.001)
autoencoder.compile(optimizer=optimizer, loss='binary_crossentropy')

import zipfile

zip_ref = zipfile.ZipFile("Zipped_final.zip", 'r')
zip_ref.extractall("/tmp")
zip_ref.close()


#Loading in the data and resizing the images
from skimage.io import imread_collection

col_dir = '/tmp/Zipped/Amazon Images/*.jpg'
col_amazon = imread_collection(col_dir)
col_amazon = list(col_amazon)

from skimage.transform import resize

for i in range(len(col_amazon)):
    col_amazon[i] = resize(col_amazon[i], (320, 192, 3))

col_dir = '/tmp/Zipped/Flipkart Images/*.jpg'
col_fk = imread_collection(col_dir)
col_fk = list(col_fk)

for i in range(len(col_fk)):
    col_fk[i] = resize(col_fk[i], (320, 192, 3))

col_dir = '/tmp/Zipped/Myntra Images/*.jpg'
col_myntra = imread_collection(col_dir)
col_myntra = list(col_myntra)

for i in range(len(col_myntra)):
    col_myntra[i] = resize(col_myntra[i], (320, 192, 3))

col_dir = '/tmp/Zipped/Pinterest Men Images/*.jpg'
col_pinmen = imread_collection(col_dir)
col_pinmen = list(col_pinmen)

for i in range(len(col_pinmen)):
    col_pinmen[i] = resize(col_pinmen[i], (320, 192, 3))

col_dir = '/tmp/Zipped/Pinterest Women Images/*.jpg'
col_pinwom = imread_collection(col_dir)
col_pinwom = list(col_pinwom)

for i in range(len(col_pinwom)):
    col_pinwom[i] = resize(col_pinwom[i], (320, 192, 3))

col_dir = '/tmp/Zipped/Vogue Images/*.jpg'
col_vog = imread_collection(col_dir)
col_vog = list(col_vog)

for i in range(len(col_vog)):
    col_vog[i] = resize(col_vog[i], (320, 192, 3))

col_clothes = col_amazon+col_fk+col_pinmen+col_vog+col_myntra+col_pinwom

x_train = np.array(col_clothes[0:3000])
x_test = np.array(col_clothes[3000:])
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

#Training the model
autoencoder.fit(x_train, x_train,
                epochs=50,
                batch_size=32,
                validation_data=(x_test, x_test))

#Saving the model
encoder = Model(input_img, encoded)
encoder.save("encoder") 
