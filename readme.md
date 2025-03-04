# Fake Image and Steganography Detection

## Project Overview
This project aims to detect fake images and steganography using a machine learning model. It consists of a *back-end* (Python Flask) and a *front-end* (Next.js) to provide a web-based interface for users to upload and analyze images.

## Features
- *Back-End*: Handles image processing and analysis using Python and a pre-trained model (test.h5).
- *Front-End*: Provides an interactive UI for users to upload and receive analysis results.
- *Docker Support*: The project is containerized using Docker for easy deployment.
- *Linux Support*: A Bash script (local-start-linux.sh) is available to run the project on Linux machines.

---

## Installation and Setup
### Prerequisites
Ensure you have the following installed:
- Docker (recommended for deployment)
- Bash (for running the script on Linux machines)
- Python 3.9+ (if running locally without Docker)
- Node.js 18+ (if running locally without Docker)
- npm (Node Package Manager, if running locally without Docker)

### Running with Docker (Recommended)
1. Clone the repository:
   bash
   git clone https://github.com/ihabaec/imtp.git
   cd imtp
   

2. Build the Docker container:
   bash
   docker build -t web-ui .
   

3. Run the container:
   bash
   docker run -p 5000:5000 -p 3000:3000 web-ui
   

4. The application should be accessible at:
   - *Back-End API*: http://localhost:5000
   - *Front-End UI*: http://localhost:3000

---

### Running on Linux (Without Docker)
Instead of manually starting each component, use the provided script:
1. Navigate to the project directory:
   bash
   cd <repository_name>
   
2. Grant execution permissions to the script:
   bash
   chmod +x local-start-linux.sh
   
3. Run the script to start both the back-end and front-end:
   bash
   ./local-start-linux.sh
   

This script automatically sets up the virtual environment, installs dependencies, and starts both servers.

If you prefer to start each service manually, follow these steps:
#### Back-End Setup (Manual)
1. Navigate to the back-end directory:
   bash
   cd back-end
   
2. Create and activate a virtual environment:
   bash
   python3 -m venv venv
   source venv/bin/activate
   
3. Install dependencies:
   bash
   pip install -r requirements.txt
   
4. Run the Flask API:
   bash
   python app.py
   

#### Front-End Setup (Manual)
1. Navigate to the front-end directory:
   bash
   cd front-end
   
2. Install dependencies:
   bash
   npm install
   
3. Start the development server:
   bash
   npx next dev
   

4. The application should be accessible at:
   - *Back-End API*: http://localhost:5000
   - *Front-End UI*: http://localhost:3000

---

## Usage
- Navigate to http://localhost:3000
- Upload an image for analysis
- View results on the web interface

---

## Project Structure

.
├── Dockerfile               # Docker configuration
├── back-end                 # Python Flask back-end
│   ├── app.py               # Main application logic
│   ├── requirements.txt     # Dependencies
-- NOTE : YOU NEED TO DOWNLOAD THE MODELS OR TRAIN THEM YOUR SELF
│   ├── venv/                # Virtual environment (not included in repo)
├── front-end                # Next.js front-end
│   ├── src/                 # Front-end source code
│   ├── public/              # Static assets
│   ├── package.json         # Front-end dependencies
│   ├── next.config.js       # Next.js configuration
│   ├── tailwind.config.js   # Tailwind CSS configuration
├── start.sh                 # Script for Docker
├── local-start-linux.sh     # Linux start script
└── README.md                # Project documentation


---

## Stopping the Servers
If running locally, press *Ctrl+C* in the terminal to stop the servers.
If using Docker, stop the container with:
bash
docker stop <container_id>


## License
This project is open-source under the MIT License.