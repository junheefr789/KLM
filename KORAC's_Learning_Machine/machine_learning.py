# -*- coding: euc-kr -*-

import tensorflow as tf
import numpy as np
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D

class picture_CNN:
    def __init__(self,class_count,train_data,train_label,val_data,val_label,learning_rate,batch_size,epoch_size):
        self.class_count = class_count
        self.train_data = train_data
        self.train_label = train_label
        self.val_data = val_data
        self.val_label = val_label
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.epoch_size = epoch_size
        self.model = None
        self.learning_history = None
        self.error=None
        
    def start_train(self):
        try:
            self.train_data = np.asarray(self.train_data, dtype= np.float32)
            self.train_label = np.asarray(self.train_label, dtype = np.float32)
            self.val_data = np.asarray(self.val_data, dtype = np.float32)
            self.val_label = np.asarray(self.val_label, dtype = np.float32)
            datagen = ImageDataGenerator(
                        rotation_range=45,
                        width_shift_range=.15,
                        height_shift_range=.15,
                        zoom_range=0.3,
                        horizontal_flip=True)
            datagen.fit(self.train_data)
        
            train_data_gen = datagen.flow(self.train_data, self.train_label, batch_size=self.batch_size, shuffle = True)
            val_data_gen = datagen.flow(self.val_data, self.val_label, batch_size = len(self.val_data)//3, shuffle = True)
            
            mobile_v2 = tf.keras.applications.MobileNetV2(input_shape=(224,224,3),
                                                   include_top=False,
                                                   weights='imagenet')
            mobile_v2.trainable = False
            
            self.model = tf.keras.Sequential([
                mobile_v2,
                GlobalAveragePooling2D(),
                Dense(512, activation='relu'),
                Dense(self.class_count, activation='softmax')
                ])
            
            otmz = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)
            early_stopping = EarlyStopping(monitor='val_loss', min_delta=0.01, patience=5, verbose=0, mode='auto')
            
            self.model.compile(otmz,
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
        
            self.learning_history = self.model.fit_generator(
                train_data_gen,
                steps_per_epoch=len(self.train_data) // self.batch_size,
                epochs=self.epoch_size,
                validation_data=val_data_gen,
                validation_steps=3,
                callbacks=[early_stopping]
            )
            
        except:
            self.error = 'error'
        
        return self.learning_history, self.model, self.error

class sound_CNN:
    def __init__(self,class_count,train_data,train_label,val_data,val_label,learning_rate,batch_size,epoch_size):
        self.class_count = class_count
        self.train_data = train_data
        self.train_label = train_label
        self.val_data = val_data
        self.val_label = val_label
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.epoch_size = epoch_size
        self.model = None
        self.learning_history = None
        self.error=None
        
    def start_train(self):
        try:
            self.train_data = np.asarray(self.train_data, dtype= np.float32)
            self.train_label = np.asarray(self.train_label, dtype = np.float32)
            self.val_data = np.asarray(self.val_data, dtype = np.float32)
            self.val_label = np.asarray(self.val_label, dtype = np.float32)
            
            
            
            self.model = tf.keras.Sequential([
                Conv2D(16, 3, padding='same', activation='relu', 
                       input_shape=(154, 168 ,3)),
                MaxPooling2D(),
                Dropout(0.2),
                Conv2D(32, 3, padding='same', activation='relu'),
                MaxPooling2D(),
                Conv2D(64, 3, padding='same', activation='relu'),
                MaxPooling2D(),
                Dropout(0.2),
                Flatten(),
                Dense(512, activation='relu'),
                Dense(self.class_count, activation='softmax')
                ])
            
            otmz = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)
            
            self.model.compile(otmz,
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
            
            
            self.learning_history = self.model.fit(
                x=self.train_data,
                y=self.train_label,
                batch_size = self.batch_size,
                epochs=self.epoch_size,
                validation_data=(self.val_data,self.val_label)
            )
            
        except BaseException as b:
            print(str(b))
            self.error = 'error'
        
        return self.learning_history, self.model, self.error

class pingpong_linear:
    def __init__(self,train,label,epoch):
        self.train = np.asarray(train)
        self.label = np.asarray(label)
        self.epoch = epoch
        self.model = None
    def start_learning(self):
        try:
            self.model = tf.keras.Sequential([
                    tf.keras.layers.Dense(32, activation='relu', input_shape=[20]),
                    tf.keras.layers.Dense(64, activation='relu'),
                    tf.keras.layers.Dense(1)
                    ])
            if self.epoch <50:
                self.epoch = int(2*self.epoch)
                optimizer = tf.keras.optimizers.Adam(0.0001)
            else:
                self.epoch = 3*self.epoch
                optimizer = tf.keras.optimizers.RMSprop(0.0001)
    
            self.model.compile(loss='mse',
                          optimizer=optimizer,
                          metrics=['mae', 'mse'])
            
            history = self.model.fit(
                                self.train, self.label,
                                epochs=self.epoch)
            return self.model
        except BaseException as b:
            print(str(b))
            return None