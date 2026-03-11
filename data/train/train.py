import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

# Load the training subset (80% of your data)
train_ds = tf.keras.utils.image_dataset_from_directory(
    'data/train/',
    validation_split=0.2, # Reserves 20% for validation
    subset="training",
    seed=123,             # Must be the same for both calls to avoid overlap
    image_size=(28, 28),
    color_mode='grayscale'
)

# Load the validation subset (the remaining 20%)
val_ds = tf.keras.utils.image_dataset_from_directory(
    'data/train/',
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(28, 28),
    color_mode='grayscale'
)

# 2. Build the Model
model = models.Sequential([
    layers.Rescaling(1./255, input_shape=(28, 28, 1)), # Normalize 0-255 to 0-1
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax') # 10 classes (0-9)
])

# 3. Compile and Train
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_ds, validation_data=val_ds, epochs=10)

# 4. Save for future use
model.save('models/digit_model.keras')
