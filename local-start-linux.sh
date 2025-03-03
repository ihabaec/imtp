#!/bin/bash

# Function to clean up and stop servers
cleanup() {
    echo "Stopping servers..."
    
    # Kill the back-end server if it's running
    if [ -n "$BACKEND_PID" ]; then
        echo "Stopping back-end server (PID: $BACKEND_PID)..."
        kill -SIGTERM "$BACKEND_PID" 2>/dev/null
        wait "$BACKEND_PID" 2>/dev/null
    fi

    # Kill the front-end server if it's running
    if [ -n "$FRONTEND_PID" ]; then
        echo "Stopping front-end server (PID: $FRONTEND_PID)..."
        kill -SIGTERM "$FRONTEND_PID" 2>/dev/null
        wait "$FRONTEND_PID" 2>/dev/null
    fi

    # Deactivate the virtual environment
    if command -v deactivate &>/dev/null; then
        echo "Deactivating virtual environment..."
        deactivate
    fi

    echo "Servers stopped."
    exit 0
}

# Trap SIGINT (Ctrl+C) and call the cleanup function
trap cleanup SIGINT

# Get the directory where the script is located
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# Navigate to the back-end directory (relative path)
cd "$SCRIPT_DIR/back-end" || { echo "Error: Could not find back-end directory"; exit 1; }

# Check if the virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."

    # Create a virtual environment
    python3 -m venv venv || { echo "Error: Failed to create virtual environment"; exit 1; }

    # Activate the virtual environment
    source venv/bin/activate || { echo "Error: Failed to activate virtual environment"; exit 1; }

    # Install dependencies from requirements.txt
    if [ -f "requirements.txt" ]; then
        echo "Installing dependencies from requirements.txt..."
        pip install --upgrade pip > /dev/null 2>&1
        pip install -r requirements.txt || { echo "Error: Failed to install dependencies"; deactivate; exit 1; }
    else
        echo "Error: requirements.txt not found in back-end directory"
        deactivate
        exit 1
    fi
else
    # Activate the virtual environment
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate || { echo "Error: Failed to activate virtual environment"; exit 1; }
    else
        echo "Error: Virtual environment activation script not found"
        exit 1
    fi
fi

# Run the Python app in the background
echo "Starting back-end server..."
python app.py &
BACKEND_PID=$!  # Save the PID of the background process

# Navigate to the front-end directory (relative path)
cd "$SCRIPT_DIR/front-end" || { echo "Error: Could not find front-end directory"; cleanup; }

# Start the front-end development server
echo "Starting front-end development server..."
npm run dev &
FRONTEND_PID=$!  # Save the PID of the background process

# Inform the user how to stop the servers
echo "Servers are running. Press Ctrl+C to stop them."

# Wait indefinitely until the user stops the script
while true; do
    sleep 1
done