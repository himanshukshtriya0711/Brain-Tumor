import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os
from tensorflow.keras.models import load_model


MODEL_PATH = r"backend\models\Brain_Tumour_Detection_Model1.h5"

def load_detection_model():
    """Load the brain tumor detection model."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    
    return load_model(MODEL_PATH)


def preprocess_image(img_path):
    """Preprocess image for model prediction"""
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize
    return img_array

def predict_tumor(model, img_array):
    """Predict brain tumor from image"""
    prediction = model.predict(img_array)
    confidence = float(np.max(prediction)) * 100  # Convert to percentage
    label = "Tumor Detected" if confidence > 50 else "No Tumor"
    return label, confidence
