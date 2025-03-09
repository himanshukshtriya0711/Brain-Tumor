import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

MODEL_PATH = r"backend\models\Brain_Tumour_Detection_Model1.h5"

# Define class labels
class_labels = ['No Tumor', 'Glioma', 'Meningioma', 'Pituitary']

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
    
    # Check if it's a tumor (any type of tumor) or not
    if predicted_class_idx == 0:
        label = "No Tumor Detected"
    else:
        # It's a tumor (Glioma, Meningioma, or Pituitary)
        label = f"Tumor Detected ({class_labels[predicted_class_idx]})"
    
    return label, confidence