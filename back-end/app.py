from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.models import load_model
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image, ImageChops, ImageEnhance
import numpy as np
import os
import tempfile


# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Suppress TensorFlow warnings
tf.get_logger().setLevel('ERROR')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Load the first TensorFlow model (for ELA-based predictions)
try:
    tf_model = load_model("test.h5")  # TensorFlow model
    print("✅ TensorFlow model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading TensorFlow model: {e}")

# Load the steganography detection PyTorch model
MODEL_PATH = "model_99_98_97_acc.pth"  # Path to the checkpoint
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define the ResNet34 model architecture
stegano_model = models.resnet34(pretrained=False)
num_ftrs = stegano_model.fc.in_features
stegano_model.fc = torch.nn.Linear(num_ftrs, 2)  # Force binary classification (2 outputs)

try:
    # Load the checkpoint
    state_dict = torch.load(MODEL_PATH, map_location=device)
    
    # Remove the `fc` layer weights from the checkpoint
    if 'fc.weight' in state_dict:
        del state_dict['fc.weight']
    if 'fc.bias' in state_dict:
        del state_dict['fc.bias']
    
    # Load the modified state_dict into the model
    stegano_model.load_state_dict(state_dict, strict=False)
    print("✅ Steganography model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading steganography model: {e}")

stegano_model.to(device)
stegano_model.eval()

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

# Preprocess the uploaded image for the TensorFlow model
def preprocess_image_tf(image):
    ela_image = convert_to_ela_image(image)
    ela_image = ela_image.resize((128, 128))
    
    # Normalize the image
    processed_image = np.array(ela_image) / 255.0
    processed_image = np.expand_dims(processed_image, axis=0)  # Add batch dimension
    return processed_image

# Preprocess the uploaded image for the PyTorch model
def preprocess_image_torch(image):
    image = image.convert("RGB")  # Ensure image is in RGB format
    transform = transforms.Compose([
        transforms.Resize((256, 256)),  # Resize to match model input size
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # Normalize based on ImageNet stats
    ])
    input_tensor = transform(image).unsqueeze(0).to(device)  # Add batch dimension
    return input_tensor

# Define the prediction route for the TensorFlow model
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
        processed_image = preprocess_image_tf(image)
        
        # Make a prediction
        prediction = tf_model.predict(processed_image)  # Use tf_model here
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

# Define the prediction route for the PyTorch steganography model
@app.route('/predict_stegano', methods=['POST'])
def predict_stegano():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Open the uploaded image
        image = Image.open(file.stream)

        # Preprocess the image
        input_tensor = preprocess_image_torch(image)

        # Make a prediction
        with torch.no_grad():
            output = stegano_model(input_tensor)
            probabilities = torch.softmax(output, dim=1)  # Convert logits to probabilities
            confidence, predicted_class = torch.max(probabilities, 1)

        # Map class indices to labels
        class_labels = ['Stego', 'Not Stego']  # Binary classification
        predicted_label = class_labels[predicted_class.item()]
        confidence_score = confidence.item()

        # Return the result
        return jsonify({
            'prediction': predicted_label,
            'confidence': confidence_score,
            'raw_prediction': probabilities.cpu().numpy().tolist()[0]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)