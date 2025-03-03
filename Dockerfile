# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the back-end files into the container
COPY back-end /app/back-end

# Install Python dependencies for the back-end
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install -r /app/back-end/requirements.txt

# Copy the front-end files into the container
COPY front-end /app/front-end

# Install Node.js and npm for the front-end
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install front-end dependencies
WORKDIR /app/front-end
RUN npm install

# Expose the ports for the back-end and front-end
EXPOSE 5000  
EXPOSE 3000  

# Start both servers using a script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Default command to run when the container starts
CMD ["/app/start.sh"]