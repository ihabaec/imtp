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

    echo "Servers stopped."
    exit 0
}

# Trap SIGINT (Ctrl+C) and call the cleanup function
trap cleanup SIGINT

# Navigate to the back-end directory
cd /app/back-end || { echo "Error: Could not find back-end directory"; exit 1; }

# Run the Python app in the background
echo "Starting back-end server..."
python app.py &
BACKEND_PID=$!  # Save the PID of the background process

# Navigate to the front-end directory
cd /app/front-end || { echo "Error: Could not find front-end directory"; cleanup; }

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