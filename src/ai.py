import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image

def predictCharacter(modelPath: str, image: Image) -> np.ndarray:
    img_array = tf.keras.utils.img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)
    
    model = load_model(modelPath)

    predictions = model.predict(img_array)
    
    return predictions
