#!/bin/bash

cleanup() {
    echo "Stopping servers..."
    
    if [ -n "$BACKEND_PID" ]; then
        echo "Stopping back-end server (PID: $BACKEND_PID)..."
        kill -SIGTERM "$BACKEND_PID" 2>/dev/null
        wait "$BACKEND_PID" 2>/dev/null
    fi

    if [ -n "$FRONTEND_PID" ]; then
        echo "Stopping front-end server (PID: $FRONTEND_PID)..."
        kill -SIGTERM "$FRONTEND_PID" 2>/dev/null
        wait "$FRONTEND_PID" 2>/dev/null
    fi

    if command -v deactivate &>/dev/null; then
        echo "Deactivating virtual environment..."
        deactivate
    fi

    echo "Servers stopped."
    exit 0
}


trap cleanup SIGINT


SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

cd "$SCRIPT_DIR/back-end" || { echo "Error: Could not find back-end directory"; exit 1; }

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."


    python3 -m venv venv || { echo "Error: Failed to create virtual environment"; exit 1; }

    source venv/bin/activate || { echo "Error: Failed to activate virtual environment"; exit 1; }


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

    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate || { echo "Error: Failed to activate virtual environment"; exit 1; }
    else
        echo "Error: Virtual environment activation script not found"
        exit 1
    fi
fi


echo "Starting back-end server..."
python app.py &
BACKEND_PID=$! 

cd "$SCRIPT_DIR/front-end" || { echo "Error: Could not find front-end directory"; cleanup; }

echo "Starting front-end development server..."
npm run dev &
FRONTEND_PID=$!  

echo "Servers are running. Press Ctrl+C to stop them."

while true; do
    sleep 1
done
