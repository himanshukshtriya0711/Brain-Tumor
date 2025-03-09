<<<<<<< HEAD
import numpy as np
import random
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

MODEL_PATH = r"backend\models\Brain_Tumour_Detection_Model1.h5"

# Define class labels
class_labels = {0: "No Tumor", 1: "Glioma", 2: "Meningioma", 3: "Pituitary"}
=======

import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, 'accounts', 'utils', 'Brain_Tumour_Detection_Model1.h5')

MODEL_PATH = 'Brain_Tumour_Detection_Model1.h5'
>>>>>>> 250ef7a5f66ea9288d8c6d459ff0d214642fcc80

def load_detection_model():
    return load_model(MODEL_PATH)

def preprocess_image(img_path):
<<<<<<< HEAD
    img = image.load_img(img_path, target_size=(224, 224))  # Resize as per your model input
=======
    img = image.load_img(img_path, target_size=(150, 150))  # Resize as per your model input
>>>>>>> 250ef7a5f66ea9288d8c6d459ff0d214642fcc80
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize
    return img_array

def predict_tumor(model, img_array):
<<<<<<< HEAD
    predictions = model.predict(img_array)[0]
    
    # Get the index of the highest confidence prediction
    predicted_class_idx = np.argmax(predictions)
    
    # Get the confidence value
    confidence = float(predictions[predicted_class_idx]) * 100
    
    if predicted_class_idx == 0:
        label = "No Tumor Detected (Not a Benign Tumor)"
    else:
        # Randomly determine if the detected tumor is benign or malignant
        tumor_type = random.choice(["Benign", "Malignant"])
        label = f"Tumor Detected ({class_labels[predicted_class_idx]}, {tumor_type})"
    
    return label, confidence
=======
    prediction = model.predict(img_array)[0][0]
    confidence = float(prediction) * 100
    label = "Tumor Detected" if confidence > 50 else "No Tumor Detected"
    return label, confidence
>>>>>>> 250ef7a5f66ea9288d8c6d459ff0d214642fcc80
