import tensorflow as tf
import tensorflow_datasets as tfds
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2



tfds.disable_progress_bar()
(raw_train, raw_validation, raw_test), metadata = tfds.load(
    'cats_vs_dogs',
    split=['train[:80%]', 'train[80%:90%]', 'train[90%:]'],
    with_info=True,
    as_supervised=True,
)

(raw_train, raw_validation, raw_test), metadata = tfds.load(
    'cats_vs_dogs',
    split=['train[:80%]', 'train[80%:90%]', 'train[90%:]'],
    with_info=True,
    as_supervised=True,
)


get_label_name = metadata.features['label'].int2str

IMG_SIZE = 160

def format_example(image, label):
    image = tf.cast(image, tf.float32)
    image = (image/127.5) - 1
    image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE))
    return image, label

train = raw_train.map(format_example)
validation = raw_validation.map(format_example)
test = raw_test.map(format_example)

BATCH_SIZE = 32
SHUFFLE_BUFFER_SIZE = 1000

train_batches = train.batch(BATCH_SIZE)
validation_batches = validation.batch(BATCH_SIZE)
test_batches = test.batch(BATCH_SIZE)

for color_image_batch, label_batch in train_batches.take(1):
    pass


color2_image_batch = []
for image in color_image_batch:
    color2 = np.asarray(image)
    color2 = cv2.cvtColor(color2,cv2.COLOR_RGB2BGR)
    color2 = color2.reshape(160,160,3)
    color2_image_batch.append(color2)
color2_image_batch = np.asarray(color2_image_batch)

cv2.imshow('test',color2_image_batch[0])
cv2.waitKey(0)


color_conv_layer = tf.keras.applications.MobileNetV2(input_shape=(160,160,3),include_top=False,
                                               weights='imagenet')

color2_conv_layer = tf.keras.applications.MobileNet(input_shape=(160,160,3),include_top=False,
                                               weights='imagenet')
color_pooling_layer = tf.keras.layers.GlobalAveragePooling2D()(color_conv_layer.output)
color2_pooling_layer = tf.keras.layers.GlobalAveragePooling2D()(color2_conv_layer.output)

concatenate_layer = tf.keras.layers.concatenate([color_pooling_layer, color2_pooling_layer])
flatten_layer = tf.keras.layers.Flatten()(concatenate_layer)

predict = tf.keras.layers.Dense(1)(flatten_layer)

model = tf.keras.Model(inputs=[color_conv_layer.input, color2_conv_layer.input], outputs=predict)
model.compile(optimizer=tf.keras.optimizers.RMSprop(lr=0.0001),
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit([color_image_batch,color2_image_batch],label_batch,epochs=10)