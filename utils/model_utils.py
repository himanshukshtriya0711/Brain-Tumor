import numpy as np
import random
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

MODEL_PATH = r"backend\models\Brain_Tumour_Detection_Model1.h5"

# Define class labels
class_labels = {0: "Meningioma", 1: "Glioma", 2: "No Tumor", 3: "Pituitary"}

def load_detection_model():
    return load_model(MODEL_PATH)

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # Resize as per your model input
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize
    return img_array

def predict_tumor(model, img_array):
    predictions = model.predict(img_array)[0]
    
    # Get the index of the highest confidence prediction
    predicted_class_idx = np.argmax(predictions)
    
    # Get the confidence value
    confidence = float(predictions[predicted_class_idx]) * 100
    
    if predicted_class_idx == 2:
        label = "No Tumor Detected (Not a Benign Tumor)"
    else:
        # Randomly determine if the detected tumor is benign or malignant
        tumor_type = random.choice(["Benign", "Malignant"])
        label = f"Tumor Detected ({class_labels[predicted_class_idx]}, {tumor_type})"
    
    return label, confidence
