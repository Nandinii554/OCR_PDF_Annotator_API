# Use official Python base image
FROM python:3.10-slim

# Install system dependencies: poppler, tesseract, and image libs
RUN apt-get update && \
    apt-get install -y poppler-utils tesseract-ocr libgl1 && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for FastAPI
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
