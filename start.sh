#!/bin/bash

cleanup() {
    echo "Stopping servers..."
    
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

    echo "Servers stopped."
    exit 0
}

trap cleanup SIGINT

cd /app/back-end || { echo "Error: Could not find back-end directory"; exit 1; }

echo "Starting back-end server..."
python app.py &
BACKEND_PID=$! 

cd /app/front-end || { echo "Error: Could not find front-end directory"; cleanup; }

echo "Starting front-end development server..."
npm run dev &
FRONTEND_PID=$!  

echo "Servers are running. Press Ctrl+C to stop them."

while true; do
    sleep 1
done
