# Use the official Python image as the base image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code into the container
COPY . .

# Expose port 8501 for Streamlit
EXPOSE 8501

# Run the command to start the app when the container starts
CMD ["streamlit", "run", "app.py"]