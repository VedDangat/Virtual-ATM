#pip install scikit-learn

import numpy as np
import argparse
import matplotlib.pyplot as plt
import cv2
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import MaxPooling2D
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import time
import os

# some_file.py
import sys

import evaluation
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

batch_size = 32
num_epoch = 50
num_class = 3


def plot_model_history(model_history):
    """
    Plot Accuracy and Loss curves given the model_history
    """
    fig, axs = plt.subplots(1,2,figsize=(15,5))
    # summarize history for accuracy
    axs[0].plot(range(1,len(model_history['history']['accuracy'])+1),model_history['history']['accuracy'])
    axs[0].plot(range(1,len(model_history['history']['val_accuracy'])+1),model_history['history']['val_accuracy'])
    axs[0].set_title('Model Accuracy')
    axs[0].set_ylabel('Accuracy')
    axs[0].set_xlabel('Epoch')
    axs[0].set_xticks(np.arange(1,len(model_history['history']['accuracy'])+1, 3))
    axs[0].legend(['train', 'val'], loc='best')
    # summarize history for loss
    axs[1].plot(range(1,len(model_history['history']['loss'])+1),model_history['history']['loss'])
    axs[1].plot(range(1,len(model_history['history']['val_loss'])+1),model_history['history']['val_loss'])
    axs[1].set_title('Model Loss')
    axs[1].set_ylabel('Loss')
    axs[1].set_xlabel('Epoch')
    axs[1].set_xticks(np.arange(1,len(model_history['history']['loss'])+1, 3))
    axs[1].legend(['train', 'val'], loc='best')
    fig.savefig('plot.png')
    plt.show()


def load_dataset(data_dir):
    X = []
    Y = []
    for category in os.listdir(data_dir):
        category_path = os.path.join(data_dir, category)
        for file_name in os.listdir(category_path):
            file_path = os.path.join(category_path, file_name)
            if not os.path.exists(file_path):
              print(file_path)
            image = cv2.imread(file_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.resize(image, (96, 96))
            X.append(image)
            Y.append(category)
    X = np.array(X)
    Y = np.array(Y)
    return X, Y

train_images, train_labels = load_dataset('FINGER DATASET FP/train')
test_images, test_labels = load_dataset('FINGER DATASET FP/test')

# Normalize the images
train_images = train_images.astype('float32') / 255
test_images = test_images.astype('float32') / 255

# Convert class vectors to binary class matrices
le = LabelEncoder()
train_labels = le.fit_transform(train_labels)
test_labels = le.transform(test_labels)

train_labels = tf.keras.utils.to_categorical(train_labels, num_class)
test_labels = tf.keras.utils.to_categorical(test_labels, num_class)

# Split training dataset into training and validation dataset
validation_split = 0.2
indices = np.random.permutation(train_images.shape[0])
train_indices = indices[:int(train_images.shape[0] * (1 - validation_split))]
val_indices = indices[int(train_images.shape[0] * (1 - validation_split)):]

val_images, val_labels = train_images[val_indices], train_labels[val_indices]
train_images, train_labels = train_images[train_indices], train_labels[train_indices]

le.classes_
train_images[0].shape, val_images[0].shape


def custom_loss(y_true, y_pred):
    # Define penalty
    penalty = 1

    # Compute cross-entropy loss
    ce_loss = tf.keras.losses.categorical_crossentropy(y_true, y_pred)

    # Compute penalty for misclassifications
    pred_labels = tf.argmax(y_pred, axis=1)
    true_labels = tf.argmax(y_true, axis=1)
    incorrect_preds = tf.not_equal(pred_labels, true_labels)
    penalty_loss = tf.cast(incorrect_preds, tf.float32) * penalty

    # Compute total loss
    total_loss = ce_loss + penalty_loss

    return total_loss

# Create the model
model = Sequential()

early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(96,96, 1))) #L1
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))  #l2
model.add(MaxPooling2D(pool_size=(2, 2)))  #  1
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))  # l3
model.add(MaxPooling2D(pool_size=(2, 2)))  # 2
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu')) # l4
model.add(MaxPooling2D(pool_size=(2, 2))) # 2
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_class, activation='softmax'))

learning_rate = 0.001
decay_rate = learning_rate / num_epoch
optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate, decay=decay_rate)


model.compile(loss=custom_loss, optimizer=optimizer,metrics=['accuracy'])
model.summary()


model_info = None
try:
  model.load_weights('model/FP_model_CNN.weights.h5')
except:
  start_time = time.time()
  model_info = model.fit(
            train_images,
            train_labels,
            epochs=num_epoch,
            batch_size=batch_size,
           # callbacks=[early_stopping],
            validation_data=(val_images, val_labels))
  end_time = time.time()
  print('Training Time: ', end_time-start_time)
  model.save_weights('model/FP_model_CNN.weights.h5')
  np.save('history.npy', model_info.history)
  
  
start_time = time.time()
model.evaluate(test_images, test_labels)
end_time = time.time()
print('Evaluation Time: ', end_time-start_time)

start_time = time.time()
Y_pred = model.predict(test_images)
end_time = time.time()
print(f'Testing Time for {len(test_images)} images: ', end_time-start_time)
y_pred = np.argmax(Y_pred, axis=1)

test_labels_t = np.argmax(test_labels, axis=1)
print('y_pred', y_pred[0])
print('y_actual', test_labels_t[0])


# evaluation.print_performance(y_pred, test_labels_t)
# evaluation.multiclass_roc_auc_score(test_labels_t, y_pred)

g = {}
model_info = { 'history': np.load('history.npy', allow_pickle=True).item() }
# if model_info == None:
#   else:
#   for key in model_info['history'].keys():
#     g[key] = model_info['history'][key]
#   model_info = {'history': g}

plot_model_history(model_info)  