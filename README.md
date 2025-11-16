# IMTP - Image Manipulation Detection

A full-stack application for detecting manipulated or fake images using Error Level Analysis (ELA) and machine learning.

## Overview

This project uses TensorFlow/Keras to analyze images and determine whether they have been manipulated or are authentic. The backend processes images using Error Level Analysis (ELA) technique and feeds them to a trained neural network model for classification.

## Tech Stack

### Backend
- **Flask** - Python web framework
- **TensorFlow/Keras** - Machine learning framework
- **PIL (Pillow)** - Image processing
- **Flask-CORS** - Cross-origin resource sharing support

### Frontend
- **Next.js 15.1.6** - React framework
- **React 18.3.1** - UI library
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **next-themes** - Theme management

## Features

- Upload images for manipulation detection
- Real-time prediction with confidence scores
- Error Level Analysis (ELA) preprocessing
- RESTful API for predictions
- Modern, responsive UI built with Next.js

## Prerequisites

- Python 3.x
- Node.js and npm
- Linux/Unix environment (for using the provided start scripts)

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd back-end
```

2. Create a virtual environment:
```bash
python3 -m venv venv
```

3. Activate the virtual environment:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd front-end
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Quick Start (Linux)

Use the provided startup script for local development:

```bash
./local-start-linux.sh
```

This script will:
- Create and activate a Python virtual environment (if needed)
- Install backend dependencies
- Start the Flask backend server on port 5000
- Start the Next.js development server
- Handle graceful shutdown with Ctrl+C

### Manual Start

#### Backend
```bash
cd back-end
source venv/bin/activate
python app.py
```

The backend API will be available at `http://localhost:5000`

#### Frontend
```bash
cd front-end
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Docker Deployment

Use the provided `start.sh` script for containerized deployment:

```bash
./start.sh
```

## API Endpoints

### POST /predict

Upload an image for manipulation detection.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Image file with key `file`

**Response:**
```json
{
  "prediction": "Real" | "Fake",
  "confidence": 0.95,
  "raw_prediction": [0.05, 0.95]
}
```

**Error Response:**
```json
{
  "error": "Error message"
}
```

## How It Works

1. **Image Upload**: User uploads an image through the frontend
2. **ELA Processing**: Backend converts the image to ELA representation to highlight compression artifacts
3. **Preprocessing**: Image is resized to 128x128 and normalized
4. **Prediction**: Trained model classifies the image as "Real" or "Fake"
5. **Results**: Confidence scores and classification are returned to the user

## Model

The application uses a pre-trained TensorFlow/Keras model (`test.h5`) that has been trained to detect image manipulations using Error Level Analysis features.

## Development

### Frontend Development
```bash
cd front-end
npm run dev      # Start development server
npm run build    # Build for production
npm run start    # Start production server
npm run lint     # Run ESLint
```

### Backend Development

The Flask backend runs with debug mode disabled in production. Modify [app.py](back-end/app.py) for development settings.

## Project Structure

```
imtp/
├── back-end/
│   ├── app.py              # Flask application
│   ├── test.h5             # Trained ML model(MODEL IS deleted, you will have to train it on your own)
│   ├── requirements.txt    # Python dependencies
│   └── venv/               # Virtual environment
├── front-end/
│   ├── package.json        # Node.js dependencies
│   └── ...                 # Next.js application files
├── local-start-linux.sh    # Local development startup script
├── start.sh                # Docker deployment script
└── README.md
```

## License

This project is private and not licensed for public use.

## Contributing

This is a private project. Contact the repository owner for contribution guidelines.
