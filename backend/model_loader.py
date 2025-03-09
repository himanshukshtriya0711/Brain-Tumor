import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os


# Define the path to your model
MODEL_PATH = r"backend\models\Brain_Tumour_Detection_Model1.h5"

# Load the model once to avoid reloading every time
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded successfully!")

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # Adjust size based on your model
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize

    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=1)[0]  # Get class index

    confidence = float(np.max(prediction))  # Get confidence score

    # Modify labels according to your dataset
    class_labels = ["No Tumor", "Tumor Detected"]  
    result = class_labels[predicted_class]

    return {"prediction": result, "confidence": confidence}
