from flask import Flask, request, jsonify
from flask_cors import CORS  
import tensorflow as tf
from tensorflow.keras.models import load_model
#from PIL import Image, ImageChops, ImageEnhance
import numpy as np
import tempfile
import os


tf.get_logger().setLevel('ERROR')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
# Load the trained TensorFlow model
model = load_model("test.h5")
stegano_model = load_model("test.h5")  # Model for detecting steganography

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Helper function for ELA conversion
def convert_to_ela_image(image, quality=90):
    temp_dir = tempfile.TemporaryDirectory()
    temp_filename = os.path.join(temp_dir.name, 'temp_file_name.jpg')
    
    # Save the original image
    image = image.convert('RGB')
    image.save(temp_filename, 'JPEG', quality=quality)
    temp_image = Image.open(temp_filename)
    
    # Calculate the ELA image
    ela_image = ImageChops.difference(image, temp_image)
    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff
    
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
    temp_dir.cleanup()
    
    return ela_image

# Preprocess the uploaded image
def preprocess_image(image):
    ela_image = convert_to_ela_image(image)
    ela_image = ela_image.resize((128, 128))
    
    # Normalize the image
    processed_image = np.array(ela_image) / 255.0
    processed_image = np.expand_dims(processed_image, axis=0)  # Add batch dimension
    return processed_image

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # Open the uploaded image
        image = Image.open(file.stream)
        
        # Preprocess the image
        processed_image = preprocess_image(image)
        
        # Make a prediction
        prediction = model.predict(processed_image)
        class_labels = ['Fake', 'Real']
        predicted_class = np.argmax(prediction[0])
        confidence = prediction[0][predicted_class]
        
        # Return the result
        return jsonify({
            'prediction': class_labels[predicted_class],
            'confidence': float(confidence),
            'raw_prediction': prediction[0].tolist()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 🔹 Route for steganography detection
@app.route('/predict_stegano', methods=['POST'])
def predict_stegano():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Open and preprocess the image
        image = Image.open(file.stream)
        processed_image = preprocess_stegano_image(image)

        # Make a prediction
        prediction = stegano_model.predict(processed_image)
        class_labels = ['Stego', 'Real']
        predicted_class = np.argmax(prediction[0])
        confidence = prediction[0][predicted_class]

        return jsonify({
            'prediction': class_labels[predicted_class],
            'confidence': float(confidence),
            'raw_prediction': prediction[0].tolist()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
