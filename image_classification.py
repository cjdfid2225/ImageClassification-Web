#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tensorflow as tf
import matplotlib.image as img
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
from collections import defaultdict
import collections
from shutil import copy
from shutil import copytree, rmtree
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras import regularizers
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D, GlobalAveragePooling2D, AveragePooling2D,GlobalMaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.regularizers import l2
from tensorflow import keras
from tensorflow.keras import models
import cv2


# #### 데이터 확인

# In[2]:


plt.rc('font', family='Malgun Gothic')
rows = 17
cols = 6
fig, ax = plt.subplots(rows, cols, figsize=(25,25))
fig.suptitle("Showing one random image from each class", y=1.05, fontsize=24) # Adding  y=1.05, fontsize=24 helped me fix the suptitle overlapping with axes issue
data_dir = "./Data/kfood/images/"
foods_sorted = sorted(os.listdir(data_dir))
food_id = 0
for i in range(rows):
  for j in range(cols):
    try:
      food_selected = foods_sorted[food_id] 
      food_id += 1
    except:
      break
    if food_selected == '.DS_Store':
        continue
    food_selected_images = os.listdir(os.path.join(data_dir,food_selected)) # returns the list of all files present in each food category
    food_selected_random = np.random.choice(food_selected_images) # picks one food item from the list as choice, takes a list and returns one random item
    img = plt.imread(os.path.join(data_dir,food_selected, food_selected_random))
    ax[i][j].imshow(img)
    ax[i][j].set_title(food_selected, pad = 10)
    
plt.setp(ax, xticks=[],yticks=[])
plt.tight_layout()


# #### 데이터 복사 (원복데이터 보존을 위해)

# In[3]:


def prepare_data(filepath, src,dest):
    classes_images = defaultdict(list) 
      with open(filepath, 'r') as txt:
        paths = [read.strip() for read in txt.readlines()]
        for p in paths:
            food = p.split('/')
            classes_images[food[0]].append(food[1] + '.jpg') 

    for food in classes_images.keys():
        print("\nCopying images into ",food)
        if not os.path.exists(os.path.join(dest,food)):
            os.makedirs(os.path.join(dest,food))
        for i in classes_images[food]:
            copy(os.path.join(src,food,i), os.path.join(dest,food,i))
            print("Copying Done!")


# In[7]:


prepare_data('./meta/train.txt', './images', 'train')


# In[ ]:


print("Creating test data...")
prepare_data('./meta/test.txt', './images', 'test')


# In[8]:


foods_sorted


# #### 많은 데이터셋을 돌리긴 컴퓨팅파워가 모자라 데이터를 자름.

# In[9]:


def dataset_mini(food_list, src, dest):
  if os.path.exists(dest):
    rmtree(dest) # 해당 폴더가 존재하면 폴더 삭제.
  os.makedirs(dest)
  for food_item in food_list :
    print("Copying images into",food_item)
    copytree(os.path.join(src,food_item), os.path.join(dest,food_item))


# In[10]:


food_list = ['갈비찜','두부김치','삼겹살']
src_train = 'train'
dest_train = 'train_mini'
src_test = 'test'
dest_test = 'test_mini'


# In[11]:


print("Creating train data folder with new classes")
dataset_mini(food_list, src_train, dest_train)


# In[12]:


print("Creating train data folder with new classes")
dataset_mini(food_list, src_test, dest_test)


# In[14]:


# %pwd


# #### pretrain model - inception v3 를 사용
# - pretrain(전이학습) 을 사용하는 이유
#     - 일반적으로 train 할때 데이터 feature를 파악하기 위해 많은 비용이 발생하는데, 전이학습을 사용하면 이를 피할 수 있다.
# 
# - inception V3 : ImageNet 이라는 데이터를 분류하는데 학습되어있다.
# 

# In[15]:


K.clear_session()
n_classes = 3
img_width, img_height = 299, 299 # inception 의 권장사항.
train_data_dir = './train_mini'
validation_data_dir = './test_mini'
nb_train_samples = 2237 #75750
nb_validation_samples = 746 #25250
batch_size = 16

# 데이터 증강.
# rotation_range = 40,        #이미지 회전 범위 (degrees)
# width_shift_range = 0.2,    #그림을 수평 또는 수직으로 랜덤하게 평행 이동시키는 범위 (원본 가로, 세로 길이에 대한 비율 값)
# height_shift_range = 0.2,    
# rescale = 1./255,             
# 원본 영상은 0-255의 RGB 계수로 구성되는데, 
# 이 같은 입력값은 모델을 효과적으로 학습시키기에 너무 높음 (통상적인 learning rate를 사용할 경우). 
# 이래서 이를 1/255로 스케일링하여 0-1 범위로 변환. 이는 다른 전처리 과정에 앞서 가장 먼저 적용.
# shear_range = 0.2,           #임의 전단 변환 (shearing transformation) 범위
# zoom_range = 0.2,           #임의 확대/축소 범위
# horizontal_flip = True,       #True로 설정할 경우, 50% 확률로 이미지를 수평으로 뒤집음. 
#  원본 이미지에 수평 비대칭성이 없을 때 효과적. 즉, 뒤집어도 자연스러울 때 사용하면 좋음.
# fill_mode = `nearest`)        #이미지를 회전, 이동하거나 축소할 때 생기는 공간을 채우는 방식

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size, # 한번 flow_from_directory 가 실행될 때 생성할 이미지 수.
    class_mode='categorical') 
#" categorical" will be 2D one-hot encoded labels, - "
#  binary" will be 1D binary labels, 
# "sparse" will be 1D integer labels, - 
# "input" will be images identical to input images (mainly used to work with autoencoders). 
# - If None, no labels are returned 

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')

# transfer learning
# include_Top = false 는 convolution layer만 가져오고 
# 추가로 Fully connected layer를 임의로 쌓을수 있다.
inception = InceptionV3(weights='imagenet', include_top=False)
x = inception.output
x = GlobalMaxPooling2D()(x)
x = Dense(128,activation='relu')(x)
x = Dropout(0.2)(x)

predictions = Dense(3,kernel_regularizer=regularizers.l2(0.005), activation='softmax')(x)

model = Model(inputs=inception.input, outputs=predictions)
# model.load('best_model_3class.hdf5')
# monetum : 적절한 방향으로 가속화하여 , 흔들림(진동)을 줄여주는 매개변수.
model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy', metrics=['accuracy'])
checkpointer = ModelCheckpoint(filepath='best_model_3class.hdf5', verbose=1, save_best_only=True)
csv_logger = CSVLogger('history_3class.log')

history = model.fit_generator(train_generator,
                    steps_per_epoch = nb_train_samples // batch_size,
                    validation_data=validation_generator,
                    validation_steps=nb_validation_samples // batch_size,
                    epochs=10,
                    verbose=1,
                    callbacks=[csv_logger, checkpointer])

model.save('model_trained_3class.hdf5')


# In[26]:


model.summary()


# In[ ]:


# keras.utils.plot_model(model, 'kfood_101_model.png',show_shape=True)


# In[20]:


def plot_accuracy(history,title):
    plt.title(title)
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train_accuracy', 'validation_accuracy'], loc='best')
    plt.show()
def plot_loss(history,title):
    plt.title(title)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train_loss', 'validation_loss'], loc='best')
    plt.show()


# In[21]:


plot_accuracy(history,'FOOD101-Inceptionv3')
plot_loss(history,'FOOD101-Inceptionv3')


# In[ ]:


print("정확도 : %.4f" % (model.evaluate(X_test, y_test)[1]))


# In[4]:


get_ipython().run_cell_magic('time', '', "K.clear_session()\nmodel_best = load_model('./Data/kfood/best15_1/best_model_15class.hdf5',compile = False)")


# In[61]:


keras.utils.plot_model(model_best, 'kfood_101_model.png')


# In[5]:


# n = 11
# food_list = pick_n_random_classes(n)
food_list = ['갈비구이', '감자전', '김밥', '김치볶음밥', '닭볶음탕', '도라지무침', '라볶이', '멍게', '백김치', '북엇국', '산낙지','생선전','알밥','오징어채볶음','콩국수']
print("These are the randomly picked food classes we will be training the model on...\n", food_list)


# In[6]:


def predict_class(model, images, show = True):
  for img in images:
    img = image.load_img(img, target_size=(299, 299))
    img = image.img_to_array(img) # 이미지를 numpy 배열로 전환해준다.            
    img = np.expand_dims(img, axis=0) # 차원증가         
    img /= 255.                                      

    pred = model.predict(img)
    index = np.argmax(pred) # accuracy 높은순으로 
    food_list.sort()
    pred_value = food_list[index]
    if show:
        plt.imshow(img[0])                           
        plt.axis('off')
        plt.title(pred_value)
        plt.show()
        print(pred_value)


# In[9]:


images=os.listdir("./Data/kfood/own_dataset")


# In[10]:


images


# In[18]:


get_ipython().run_line_magic('pwd', '')
get_ipython().run_line_magic('cd', './Data/kfood/own_dataset')


# In[19]:


# 갈비구이_감자전_김밥_김치볶음밥_닭볶음탕_도라지무침_라볶이_멍게_백김치_북엇국_산낙지_생선전_알밥_오징어채볶음_콩국수
# images = []
# images.append('./갈비구이1.jpg')
# images.append('./삼겹살1.jpg')
# images.append('./떡볶이1.jpg')
# images.append('./갈비찜1.jpg')
predict_class(model_best, images, True)


# In[ ]:




