from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import os

#Face Emotion Recognition Inspiration Idea
#https://youtu.be/aoCIoumbWQY?si=SSjJzWe2PdHmK1js
#https://youtu.be/avv9GQ3b6Qg?si=ginbyJzbel0VTQYK

# Data augmentation and normalization for training and validation datasets
train = ImageDataGenerator(rescale = 1./255)

# Loading the training dataset from the directory
train_dataset = train.flow_from_directory(r"D:\\OneDrive\\Desktop\\G7_FinalProject\\BaseData\\training\\",
                                        target_size = (400,400),
                                        batch_size = 64,
                                        class_mode = 'categorical',
                                        subset='training')

# Check class indices in the training dataset
train_dataset.class_indices

# Building the CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(400, 400, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(6, activation='softmax')  # 6 classes: happy, sad, fear, surprise, disgusting, angry
])

# Compiling the model with optimizer, loss function, and metrics
model.compile(optimizer = 'Nadam',
              loss = 'MSE',
              metrics = ['accuracy'])

# Training the model
model_info = model.fit(train_dataset,
                      steps_per_epoch = train_dataset.samples//train_dataset.batch_size,
                      epochs=30
                    )

# Saving the trained model
model.save('emotion_detection_model')

# Extracting accuracy and loss data for visualization
acc = model_info.history['accuracy']
loss = model_info.history['loss']
epochs_range = range(30)

# Plotting training accuracy and loss
plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, loss, label='Training Loss')
plt.legend(loc='lower right')
plt.title('Training Accuracy and Loss')
plt.show()