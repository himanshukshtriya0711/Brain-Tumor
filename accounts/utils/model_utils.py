
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, 'accounts', 'utils', 'Brain_Tumour_Detection_Model1.h5')

MODEL_PATH = 'Brain_Tumour_Detection_Model1.h5'

def load_detection_model():
    return load_model(MODEL_PATH)

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(150, 150))  # Resize as per your model input
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize
    return img_array

def predict_tumor(model, img_array):
    prediction = model.predict(img_array)[0][0]
    confidence = float(prediction) * 100
    label = "Tumor Detected" if confidence > 50 else "No Tumor Detected"
    return label, confidence
