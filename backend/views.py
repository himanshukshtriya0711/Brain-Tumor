import numpy as np
import tensorflow as tf
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import io
import base64

# Load the model (Make sure the path is correct)
MODEL_PATH = r"backend\models\Brain_Tumour_Detection_Model1.h5"

model = tf.keras.models.load_model(MODEL_PATH)

@csrf_exempt

def predict_image(request):
    if request.method == "POST":
        try:
            # Get the image from the request
            image_data = request.FILES.get("scan_image")  # Get uploaded file
            if not image_data:
                return JsonResponse({"error": "No image provided"}, status=400)
            
            # Convert the image to a format the model can understand
            image = Image.open(image_data).convert("RGB")
            image = image.resize((224, 224))  # Resize based on your model's input size
            image_array = np.array(image) / 255.0  # Normalize the image
            image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

            # Make prediction
            prediction = model.predict(image_array)
            confidence = float(prediction[0][0]) * 100  # Assuming single output neuron

            return JsonResponse({
                "prediction": "Tumor Detected" if confidence > 50 else "No Tumor",
                "confidence": confidence
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"message": "Send a POST request with an image."})
