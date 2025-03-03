# from flask import Flask, request, jsonify
# from flask_cors import CORS  # Import CORS
# import numpy as np
# import cv2
# import tensorflow as tf
# import requests
# import os
# import tensorflow as tf

# # Load the model from the local path
# model_path = "./ssd_mobilenet_v2"
# model = tf.saved_model.load(model_path)

# print("Model loaded successfully from local path")

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Load COCO-SSD model
# model = tf.saved_model.load("https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2")

# # Google Search API configuration
# GOOGLE_API_KEY = "AIzaSyBuW6-lpiUXWi3NIGHajbbv_xj6XfLZbAQ"
# GOOGLE_CX = "f59b0b725176c4cf8"

# # Ingredient detection route
# @app.route('/detect', methods=['POST'])
# def detect_ingredients():
#     file = request.files['file']
#     img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

#     # Preprocess the image for COCO-SSD
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     img_resized = cv2.resize(img_rgb, (300, 300))  # Resize to model's expected size
#     input_tensor = np.expand_dims(img_resized / 255.0, axis=0)

#     # Perform object detection
#     detections = model(input_tensor)

#     # Extract detection results
#     detected_classes = detections['detection_classes'][0].numpy()
#     detected_scores = detections['detection_scores'][0].numpy()
#     detected_boxes = detections['detection_boxes'][0].numpy()

#     # Map class IDs to COCO names
#     coco_labels = {
#         1: "person", 2: "bicycle", 3: "car", 4: "motorcycle", 5: "airplane", 6: "bus",
#         52: "apple", 53: "orange", 54: "banana", 55: "carrot", 56: "broccoli", 57: "cake"
#         # Add more as needed
#     }

#     ingredients = []
#     for i in range(len(detected_classes)):
#         if detected_scores[i] >= 0.5:  # Confidence threshold
#             class_id = int(detected_classes[i])
#             name = coco_labels.get(class_id, "unknown")
#             bbox = detected_boxes[i]

#             # Simulated quantity estimation
#             estimated_volume_ml = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) * 1000
#             quantity = "Medium (~200-500g)" if estimated_volume_ml > 300 else "Small (<200g)"

#             ingredients.append({"name": name, "quantity": quantity})

#     return jsonify({"ingredients": ingredients})

# # Recipe search route
# @app.route('/search_recipes', methods=['POST'])
# def search_recipes():
#     ingredients = request.json.get('ingredients', [])
#     query = "recipes with " + ", ".join(ingredients)

#     # Perform Google Search
#     url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_CX}&q={query}"
#     response = requests.get(url)

#     if response.status_code == 200:
#         results = response.json().get('items', [])
#         recipes = [{"title": item['title'], "link": item['link'], "snippet": item['snippet']} for item in results]
#         return jsonify({"recipes": recipes})
#     else:
#         return jsonify({"error": "Failed to fetch recipes"}), 500

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import torch
import numpy as np
import cv2
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Google Search API configuration
GOOGLE_API_KEY = "AIzaSyBuW6-lpiUXWi3NIGHajbbv_xj6XfLZbAQ"
GOOGLE_CX = "f59b0b725176c4cf8"

# Ingredient detection route
@app.route('/detect', methods=['POST'])
def detect_ingredients():
    file = request.files['file']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    results = model(img)
    detected_items = results.pandas().xyxy[0]  # Detected items with bounding boxes

    ingredients = []
    for _, row in detected_items.iterrows():
        name = row['name']
        # Simulated quantity estimation
        quantity = "Medium (~200-500g)" if row['confidence'] > 0.5 else "Small (<200g)"
        ingredients.append({"name": name, "quantity": quantity})

    return jsonify({"ingredients": ingredients})

# Recipe search route
@app.route('/search_recipes', methods=['POST'])
def search_recipes():
    ingredients = request.json.get('ingredients', [])
    query = "recipes with " + ", ".join(ingredients)

    # Perform Google Search
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_CX}&q={query}"
    response = requests.get(url)

    if response.status_code == 200:
        results = response.json().get('items', [])
        recipes = [{"title": item['title'], "link": item['link'], "snippet": item['snippet']} for item in results]
        return jsonify({"recipes": recipes})
    else:
        return jsonify({"error": "Failed to fetch recipes"}), 500

if __name__ == "__main__":
    app.run(debug=True)